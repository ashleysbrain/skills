# W5 Runtime Strategies Summary

## Three-Tier Runtime Model

| Tier | Use Case | Tech Stack | Security | Cost |
|------|----------|------------|----------|------|
| T1 | Trusted artifacts, lightweight demos, static visualizations | Hugging Face Spaces (Gradio/Streamlit) | Quarterly audits, report abuse, block paid API abuse | $0 (creators pay) |
| T2 | Interactive demos with state, Jupyter notebooks, custom frameworks | Modal sandbox ephemeral containers | Network policy (block outbound except FHIR), 2 vCPUs/4GB RAM limits, 5 concurrent sessions/user | Modal free tier covers MVP; ~$880/month at 2,000 MAU |
| T3 | Creator-maintained dashboards, existing deployments, beta artifacts | Self-hosted iframes (Vercel, Railway, AWS, etc.) | CSP headers, HTTPS required, annual security questionnaire | $0 |

## Artifact Type Mapping

| Artifact | Tier | Runtime | PoC Weeks |
|----------|------|---------|-----------|
| Coach Config | T1 | Gradio chat on HF Spaces | 2 |
| Methodology | T2 | Jupyter Voila in Modal | 3 |
| Dashboard | T2/T3 | Streamlit in Modal OR self-hosted React | 4 |
| Data Recipe | T1 | Gradio Code viewer on HF Spaces | 1 |
| Health Journey | T1 | Static HTML/Gradio on HF Spaces | 1 |

## Key Security Decisions

- All demos sandboxed, no outbound internet except to FHIR service
- Modal resource limits: max 2 vCPUs, 4GB RAM per session
- Session isolation: no shared state between users
- Self-hosted iframes: CSP headers restrict to creator domain only

## Cost Projections

### MVP (first 6 months)
- 500 MAU, 2 demos/user, 5 min avg session
- Total compute: ~833 hours/month
- Modal cost after free tier: ~$220/month
- Total infra: ~$420/month (Modal + FHIR)

### Year 1 (conservative)
- 2,000 MAU by month 12
- Modal cost: ~$880/month
- FHIR service: ~$200/month
- Total: ~$1,080/month

## Scaling Triggers

1. Modal plan upgrade: > 100 MAU running 2 demos each (exhausts free tier)
2. HF Spaces → self-hosted: > 1% downtime reported by users
3. Demo queue: > $500/month Modal costs (abuse prevention)

## 14-Week Deployment Roadmap for Poojitha's Team

| Phase | Weeks | Deliverable |
|-------|-------|-------------|
| 0 | 1 | Infra setup (Modal, HF org, Next.js Modal SDK, FHIR network policy) |
| 1 | 2-3 | Coach Config MVP (template, wizard integration, HF embed, 3 samples) |
| 2 | 4-6 | Methodology MVP (template, Modal Voila, notebook streaming, 2 samples) |
| 3 | 7-10 | Dashboard MVP (Streamlit template, Modal integration, self-hosted support, 2 samples) |
| 4 | 11-12 | Data Recipe + Health Journey (templates, static viewers, testing) |
| 5 | 13-14 | Polish + Launch (load testing, analytics, docs, public launch) |

**Team composition:**
- 1 Full-stack engineer (Next.js + React)
- 1 Python/ML engineer (Gradio + Modal + FHIR)
- 0.5 DevOps engineer (Modal + CI/CD)
- 0.5 QA engineer (testing across artifact types)

## Open Questions for W6

1. Modal app ID strategy: Single app with function routing vs per-artifact apps?
2. HF Spaces vs Modal for Coach Config: Support both or start HF-only?
3. Demo session limits: 10 min too short for methodologies?
4. FHIR client credentials distribution: Modal Secrets per artifact type?
5. Analytics opt-in: Default on with notice vs explicit opt-in?