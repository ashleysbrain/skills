# Organ Implementation Verification Checklist

## Pre-Change Verification
- [ ] Backup current documentation and code
- [ ] Note current engine status (ports running, processes active)
- [ ] Identify all files that need modification:
  - Organ class definition file
  - Organ registry/dictionary
  - Documentation files
  - Diagram files (if applicable)
  - Configuration files (if applicable)

## Implementation Verification
### Code Changes
- [ ] Organ class includes all required fields:
  - `name` (organ's common name)
  - `scientist` (format: "DS [LastName]")
  - `scientist_full` (full name with lifespan)
  - `discovery` (what they discovered + year)
  - `brain_region` (if used in your implementation)
  - `creative_role` (if used in your implementation)
  - `phi_application` (if used in your implementation)
- [ ] Organ registry uses scientist-based key: `ds_[discovererlastname]`
- [ ] No syntax errors in updated code files
- [ ] Code follows existing style conventions

### Documentation Changes
- [ ] All organ sections follow the standard table format
- [ ] Table includes all required fields: Scientist, Port, Body System, Agent, Physics, Philosophy
- [ ] Scientist field uses format: "DS [LastName] (Full Name)"
- [ ] Port field is accurate (specific port or "Part of [Engine] Engine ([port])")
- [ ] Body System field accurately describes biological location
- [ ] Agent field uses correct DS agent name
- [ ] Physics field describes relevant phi-based or other principle
- [ ] Philosophy field references scientist's key contribution/philosophy
- [ ] "What it does" section is concise and action-oriented
- [ ] "Key capabilities" section has 3-5 specific bullet points
- [ ] "Connection to [Project]" section explains specific relevance
- [ ] No generic explanations or tutorial-style content
- [ ] No narrative paragraphs where bullet points or tables would be clearer

### Diagram and Table Updates
- [ ] System diagrams show correct organ names with scientist prefixes
- [ ] Signal flow diagrams include scientist names in parentheses after organ names
- [ ] Communication pathway tables reference correct organ names
- [ ] All port numbers in diagrams match implementation
- [ ] Diagram elements are properly aligned and readable

## Post-Change Verification
### Engine Status
- [ ] All dependent engines are running (check relevant ports)
- [ ] No new error messages in engine logs
- [ ] Memory usage and CPU usage within normal ranges

### Functional Testing
- [ ] Organ can be imported/instantiated without errors
- [ ] Organ fields return expected values
- [ ] Organ integrates correctly with parent engine/system
- [ ] Downstream systems that depend on this organ function correctly
- [ ] API endpoints (if applicable) respond correctly

### Documentation Validation
- [ ] Documentation renders correctly in target format (markdown, etc.)
- [ ] All links and references are valid
- [ ] No broken image or diagram references
- [ ] Consistent styling with rest of documentation

### Integration Testing
- [ ] Creative organism pipeline functions correctly with new/updated organ
- [ ] Signal flow between organs works as expected
- [ ] Output quality meets expected standards
- [ ] No regressions in related functionality

## Sign-Off
- [ ] All checklist items completed
- [ ] Changes committed with descriptive message
- [ ] Team notified of changes (if applicable)
- [ ] Verification completed by: ___________________
- [ ] Date: ___________________