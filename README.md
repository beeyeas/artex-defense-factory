# ARTEX Defense & Detection Engineering Factory

A defensive multi-agent and policy-as-code framework engineered to detect, throttle, and prevent machine-speed autonomous offensive agents (such as ARTEX-style worker swarms) across cloud control planes, identity providers, and CI/CD repositories.

## Core Capabilities
1. **Behavioral & Machine-Tempo Detection:** Identifies burst enumeration rhythms (e.g., 20+ distinct IAM/API discovery calls within <30 seconds interspersed with LLM reasoning latency pauses) via Google SecOps (YARA-L) and Sigma rules.
2. **Preventive Policy-as-Code (OPA/Rego):** Blocks unrotated personal access tokens (PATs), overly permissive cross-account `sts:AssumeRole` trust policies, and non-ephemeral machine credentials before deployment.
3. **Autonomous Blue-Team Triage Agents:** Markdown-defined defensive sub-agents that correlate high-velocity API telemetry, isolate compromised service accounts, and open automated remediation pull requests.

## Repository Structure
```text
artex-defense-factory/
├── README.md
├── agents/
│   └── blue-team/
│       └── agent-swarm-hunter.md          # Autonomous defensive sub-agent specification
├── detections/
│   ├── yara-l/
│   │   └── artex_machine_tempo_recon.yaral # Google SecOps high-velocity API burst rule
│   └── sigma/
│       └── github_pat_burst_enumeration.yml # SIEM detection for repo/token scraping
├── prevention/
│   └── opa/
│       └── iam_and_token_guardrails.rego   # Policy-as-code blocking long-lived tokens & wildcards
├── workflows/
│   └── defense_orchestrator.py            # State machine for telemetry triage & auto-containment
└── docs/
    └── threat_model.md                    # Defensive mapping against ARTEX dual-graph attack patterns
```
