---
name: conversation-archival-before-compression
description: Prevent conversation loss by archiving complete conversation state before context compression triggers
tags: [compression, archival, conversation-preservation, gateway, telegram]
version: 2.0
created: 2026-03-25
---

# Conversation Archival Before Compression

## When to Use

- User expresses concern about losing conversation data at compression
- Building long-running chat systems (Telegram, Discord, Slack gateways)
- Implementing conversation preservation for compliance/audit
- Need to recover full context after compression has occurred
- Want to catalog decision history across compressed sessions

## The Problem

Context compression is necessary for long conversations (saves tokens, prevents API failures), but it discards information. The standard `context_compressor.py` summarizes middle turns, but summaries lose:
- Exact wording of decisions
- Work artifacts produced
- Nuanced discussion that led to choices
- Full tool call sequences

Users who rely on conversation history need a way to preserve EVERYTHING before compression throws it away.

## Solution Architecture

### CRITICAL: Double Archival System (v2.0)

**USER CORRECTION (the principal, 2026-03-25):** Single archive at 85% is NOT zero loss. The last 15% (85%-100%) gets lost when compression runs.

**Solution: Archive TWICE**

1. **Warning Threshold (70%)** — notify user, no action
2. **Early Warning Archive (85%)** — first archive, alerts compression approaching
3. **Final Complete Archive (100%)** — second archive RIGHT before compression, captures EVERYTHING including last 15%
4. **Compression runs** — after both archives saved

This ensures TRUE zero data loss. Both archives are preserved:
- Early warning (85%): `{session_id}.json` 
- Final complete (100%): `{session_id}-FINAL.json`

### What to Archive

Complete conversation state in both machine and human-readable formats:

**JSON (machine-readable):**
```json
{
  "meta": {
    "session_id": "telegram-20260325-103045",
    "archived_at": "2026-03-25T10:30:45",
    "current_tokens": 42500,
    "threshold_tokens": 50000,
    "usage_percent": 85.0,
    "reason": "pre_compression_archival"
  },
  "conversation": {
    "message_count": 156,
    "messages": [/* full message array */]
  },
  "context": {/* session metadata */},
  "artifacts": [/* files created, reports generated */],
  "decisions": [/* extracted key decisions */],
  "continuation_plan": {/* how to resume after compression */}
}
```

**Markdown (human-readable):**
- Token usage summary
- Key decisions list
- Work artifacts produced
- Continuation plan

### Implementation Steps

#### 1. Create the Archival Script

Location: `~/[project]/scripts/pre-compression-archival.py`

```python
#!/usr/bin/env python3
"""Pre-compression conversation archival system."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Thresholds (match context_compressor.py)
COMPRESSION_THRESHOLD = 0.50  # 50% of context
PRE_ARCHIVE_THRESHOLD = 0.85  # Archive at 85% of compression point
WARNING_THRESHOLD = 0.70      # Warn at 70%

class ConversationArchiver:
    def __init__(self, session_id: str, archive_dir: Path):
        self.session_id = session_id
        self.archive_path = archive_dir / f"{session_id}.json"
        self.archive_path.parent.mkdir(parents=True, exist_ok=True)
    
    def should_archive(self, current_tokens: int, threshold_tokens: int, is_final: bool = False) -> bool:
        """Check if archive needed. is_final=True checks for 100%, False for 85%."""
        threshold = 1.00 if is_final else PRE_ARCHIVE_THRESHOLD
        return (current_tokens / threshold_tokens) >= threshold
    
    def archive_conversation(
        self,
        messages: List[Dict[str, Any]],
        current_tokens: int,
        threshold_tokens: int,
        metadata: Dict[str, Any] = None,
        is_final: bool = False
    ) -> str:
        """Archive full conversation with metadata. is_final=True creates final archive at 100%."""
        # Use -FINAL suffix for final archives
        if is_final:
            self.archive_path = self.archive_path.parent / f"{self.session_id}-FINAL.json"
        
        archive_data = {
            "meta": {
                "session_id": self.session_id,
                "archived_at": datetime.now().isoformat(),
                "current_tokens": current_tokens,
                "threshold_tokens": threshold_tokens,
                "usage_percent": (current_tokens / threshold_tokens) * 100,
                "reason": "final_pre_compression" if is_final else "early_warning_archive",
                "archive_type": "FINAL_COMPLETE" if is_final else "EARLY_WARNING"
            },
            "conversation": {
                "message_count": len(messages),
                "messages": messages
            },
            "context": metadata or {},
            "artifacts": self._extract_artifacts(messages),
            "decisions": self._extract_decisions(messages),
            "continuation_plan": self._generate_continuation_plan(messages)
        }
        
        # Write JSON
        with open(self.archive_path, 'w', encoding='utf-8') as f:
            json.dump(archive_data, f, indent=2, ensure_ascii=False)
        
        # Write Markdown summary
        self._write_markdown_summary(archive_data)
        
        return str(self.archive_path)
    
    def _extract_artifacts(self, messages: List[Dict]) -> List[Dict]:
        """Find work products: files created, reports generated."""
        artifacts = []
        for msg in messages:
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                if "MEDIA:" in content or "created" in content.lower():
                    artifacts.append({
                        "type": "work_product",
                        "content": content[:500],
                        "timestamp": msg.get("timestamp")
                    })
        return artifacts
    
    def _extract_decisions(self, messages: List[Dict]) -> List[str]:
        """Extract key decisions from conversation."""
        decisions = []
        keywords = ["decided", "will", "must", "requirement", "mandate", "critical"]
        
        for msg in messages:
            if msg.get("role") in ["user", "assistant"]:
                content = str(msg.get("content", ""))
                for keyword in keywords:
                    if keyword in content.lower():
                        sentences = content.split(". ")
                        for sent in sentences:
                            if keyword in sent.lower():
                                decisions.append(sent[:200])
                                break
        return list(set(decisions))[:20]
    
    def _generate_continuation_plan(self, messages: List[Dict]) -> Dict:
        """Plan for continuing after compression."""
        last_user_msg = None
        last_assistant_msg = None
        
        for msg in reversed(messages):
            if msg.get("role") == "user" and not last_user_msg:
                last_user_msg = msg.get("content", "")
            elif msg.get("role") == "assistant" and not last_assistant_msg:
                last_assistant_msg = msg.get("content", "")
            if last_user_msg and last_assistant_msg:
                break
        
        return {
            "last_user_request": last_user_msg[:500] if last_user_msg else None,
            "last_agent_response": last_assistant_msg[:500] if last_assistant_msg else None,
            "next_steps": "Review archive before continuing. Check artifacts and decisions."
        }
    
    def _write_markdown_summary(self, archive_data: Dict):
        """Human-readable summary."""
        md_path = self.archive_path.with_suffix('.md')
        
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(f"# Conversation Archive: {self.session_id}\n\n")
            f.write(f"**Archived:** {archive_data['meta']['archived_at']}\n")
            f.write(f"**Token Usage:** {archive_data['meta']['usage_percent']:.1f}%\n")
            f.write(f"**Message Count:** {archive_data['conversation']['message_count']}\n\n")
            
            f.write("## Key Decisions\n\n")
            for decision in archive_data['decisions']:
                f.write(f"- {decision}\n")
            
            f.write("\n## Work Artifacts\n\n")
            for artifact in archive_data['artifacts']:
                f.write(f"- {artifact['content'][:200]}...\n")
            
            f.write("\n## Continuation Plan\n\n")
            plan = archive_data['continuation_plan']
            f.write(f"**Last Request:** {plan['last_user_request']}\n\n")
            f.write(f"**Next Steps:** {plan['next_steps']}\n")
```

#### 2. Integrate into Gateway

**File:** `<agent-home>/hermes-agent/gateway/run.py`

**Location:** In the session hygiene compression block (search for `"Session hygiene:"` and `_needs_compress`)

**Before compression runs, add:**

```python
# Add to imports at top
import sys
from pathlib import Path
sys.path.append(str(Path.home() / "your-project/scripts"))
from pre_compression_archival import ConversationArchiver

# In session hygiene block (around line 2060-2100):
# DOUBLE ARCHIVAL: Archive at BOTH 85% and 100%
if _needs_compress or _approx_tokens >= (_compress_token_threshold * 0.85):
    try:
        archiver = ConversationArchiver(
            session_id=session_key,
            archive_dir=Path.home() / "your-project/conversations/archives"
        )
        
        # Determine if this is final (100%) or early warning (85%)
        _is_final = _needs_compress
        
        if archiver.should_archive(_approx_tokens, _compress_token_threshold, is_final=_is_final):
            archive_path = archiver.archive_conversation(
                messages=history,
                current_tokens=_approx_tokens,
                threshold_tokens=_compress_token_threshold,
                metadata={
                    "platform": platform_name,
                    "user_id": user_id,
                    "chat_id": chat_id
                },
                is_final=_is_final
            )
            
            _archive_type = "FINAL_COMPLETE" if _is_final else "EARLY_WARNING"
            logger.info(
                "Pre-compression archive [%s]: %s (tokens: %d/%d, %.1f%%)",
                _archive_type,
                Path(archive_path).name,
                _approx_tokens,
                _compress_token_threshold,
                (_approx_tokens / _compress_token_threshold) * 100
            )
            
            # Different notification for early vs final
            if _is_final:
                msg = (
                    f"🔒 FINAL ARCHIVE: Complete conversation preserved\n"
                    f"Archive: {Path(archive_path).name}\n"
                    f"This captures 100% of conversation before compression"
                )
            else:
                msg = (
                    f"⚠️ EARLY WARNING ARCHIVE: Approaching compression\n"
                    f"Archive: {Path(archive_path).name}\n"
                    f"Final complete archive will be created at 100%"
                )
            await send_message(msg)
    except Exception as e:
        logger.error("Pre-compression archival failed: %s", e, exc_info=True)

if _needs_compress:
    # Existing compression logic continues unchanged
    logger.info("Session hygiene: compressing...")
```

#### 3. Test Before Deployment

```bash
# Test the script standalone
cd ~/your-project/scripts
python3 pre-compression-archival.py

# Check archives were created
ls -lh ~/your-project/conversations/archives/

# Test gateway integration
# Start gateway and send messages until 70% threshold
# Verify warning appears
# Continue to 85% threshold
# Verify archive is created and notification sent
```

### Integration Points

**Where this hooks in:**
- `gateway/run.py`: Session hygiene compression (line ~2060)
- `run_agent.py`: CLI agent loop (optional, for CLI mode)
- `batch_runner.py`: Batch processing (if preserving batch conversations)

**Key gateway variables:**
- `_approx_tokens`: Current token estimate
- `_compress_token_threshold`: Threshold for compression
- `history`: Full message list from session_store
- `session_key`: Unique session identifier

### Common Pitfalls

1. **DON'T archive only at 85%** — YOU WILL LOSE THE LAST 15%. Archive TWICE (85% + 100%)
2. **DON'T break compression if archival fails** — wrap in try-except
3. **DON'T archive on every message** — only when threshold exceeded
4. **DON'T forget to create archive directory** — use `mkdir(parents=True, exist_ok=True)`
5. **DON'T use fixed message counts** — token-based thresholds are correct
6. **DON'T skip the markdown output** — users need human-readable format
7. **DO notify the user TWICE** — once at 85% (warning), once at 100% (final)
8. **DO use different filenames** — early: `{id}.json`, final: `{id}-FINAL.json`
9. **DO use delegation for the integration** — patching gateway code is surgical work

**CRITICAL:** Single archive at 85% means data loss. Users WILL notice and call you out. Always implement double archival.

### Verification

After integration, test with:

```python
# Create a long conversation that approaches threshold
# Monitor logs for:
# - "Pre-compression archive saved" messages
# - Archive file creation
# - User notifications

# Verify archive contents:
import json
with open("path/to/archive.json") as f:
    data = json.load(f)
    
assert "meta" in data
assert "conversation" in data
assert "artifacts" in data
assert "decisions" in data
assert data["meta"]["usage_percent"] >= 85.0
```

## Related Systems

- **context_compressor.py** — Standard compression system this augments
- **session_store** — Provides message history for archival
- **MEMORY GUARDIAN** — Can index archives for search
- **VITALS** — Can monitor archive system health
- **Live chat thread mirror pattern** — See `references/chat-thread-mirror.md` for keeping a local markdown mirror that scheduled synthesis jobs can read alongside the live thread context.

## Success Criteria

1. Archives created automatically at 85% threshold
2. User receives notification with archive location
3. Zero conversation data loss
4. Compression still runs normally (archival is additive)
5. Archives are human-readable (markdown) and machine-readable (JSON)

## Notes

- Archive is ADDITIVE to compression, not a replacement
- Thresholds match `context_compressor.py` defaults (50% base)
- Archive location should be version-controlled if critical
- Consider backup strategy for archive directory
- For compliance: disable compression, use archival only
