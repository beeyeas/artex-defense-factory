# Defensive Threat Model: Countering ARTEX-Style Agentic Swarms

## 1. Adversary Architecture Overview
Autonomous offensive frameworks like ARTEX replace slow, manual operator workflows with parallelized agent loops:
- **Asset Graph Mapping:** Rapidly enumerates domains, cloud accounts, IAM roles, and exposed repositories.
- **Exploration Graph Chaining:** Dynamically pivots from leaked credentials (e.g., unrotated GitHub PATs) to cloud control plane enumeration (`sts:GetCallerIdentity` -> `iam:List*`) within seconds.

## 2. Three-Layer Defense-in-Depth Strategy

### Layer 1: Structural Prevention (Starving the Asset Graph)
- **Eliminate Long-Lived Credentials:** Enforce OPA/Rego policies (`prevention/opa/iam_and_token_guardrails.rego`) prohibiting static IAM keys and classic personal access tokens.
- **Shorten Session Lifetimes:** Cap STS and OIDC token durations at <= 1 hour so multi-round planner/worker loops expire mid-campaign.

### Layer 2: Behavioral & Tempo Detection (Spotting the Exploration Graph)
- **Machine-Tempo Analytics:** Human operators rarely execute 25+ distinct discovery API calls in 23 seconds. Deploy `detections/yara-l/artex_machine_tempo_recon.yaral` in Google SecOps to flag high-velocity bursts.
- **Repository Audit Monitoring:** Use `detections/sigma/github_pat_burst_enumeration.yml` to detect automated PAT scraping across organization repositories.

### Layer 3: Automated Containment (Blue-Team Swarm Response)
- **Deterministic Pre-Filtering + LLM Triage:** Use `workflows/defense_orchestrator.py` to validate burst cadence deterministically, then invoke `agents/blue-team/agent-swarm-hunter.md` to correlate affected principals and revoke active sessions automatically.
