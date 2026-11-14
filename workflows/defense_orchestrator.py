"""
Defensive Orchestrator State Machine for ARTEX Swarm Detection & Containment.
Ingests high-velocity telemetry alerts, invokes the Blue-Team Hunter sub-agent,
validates containment guardrails, and dispatches automated session revocation.
"""

from pathlib import Path
from typing import TypedDict, List, Dict, Any
import json


class DefenseState(TypedDict):
    incident_id: str
    telemetry_batch: List[Dict[str, Any]]
    hunter_blueprint: str
    triage_result: Dict[str, Any]
    containment_status: str


def initialize_defense_workflow(incident_id: str, telemetry_batch: List[Dict[str, Any]]) -> DefenseState:
    blueprint_path = Path(__file__).parent.parent / "agents" / "blue-team" / "agent-swarm-hunter.md"
    return DefenseState(
        incident_id=incident_id,
        telemetry_batch=telemetry_batch,
        hunter_blueprint=blueprint_path.read_text(encoding="utf-8"),
        triage_result={},
        containment_status="INIT",
    )


def evaluate_machine_tempo(state: DefenseState) -> DefenseState:
    """
    Deterministic pre-filter: checks if telemetry exhibits ARTEX-like machine tempo
    (e.g., >= 20 distinct API calls within <= 30 seconds) before invoking LLM triage.
    """
    events = state["telemetry_batch"]
    if not events:
        state["containment_status"] = "NO_DATA"
        return state

    distinct_apis = {e.get("event_name") for e in events if e.get("event_name")}
    duration_sec = max((e.get("timestamp", 0) for e in events), default=0) - min(
        (e.get("timestamp", 0) for e in events), default=0
    )

    if len(distinct_apis) >= 20 and duration_sec <= 30:
        state["containment_status"] = "HIGH_VELOCITY_ANOMALY_CONFIRMED"
    else:
        state["containment_status"] = "NORMAL_CADENCE"
    return state


def enforce_containment_guardrails(state: DefenseState, raw_agent_json: str) -> DefenseState:
    """Parses Blue-Team Hunter JSON output and enforces human-in-the-loop approval gates."""
    try:
        result = json.loads(raw_agent_json)
        state["triage_result"] = result
        actions = result.get("recommended_containment", [])

        if any(act.get("requires_human_approval", True) for act in actions):
            state["containment_status"] = "AWAIT_HUMAN_APPROVAL"
        elif result.get("confidence_score", 0.0) >= 0.90:
            state["containment_status"] = "AUTO_CONTAINMENT_DISPATCHED"
        else:
            state["containment_status"] = "ESCALATE_TO_SOC_TIER2"
    except json.JSONDecodeError:
        state["containment_status"] = "SCHEMA_VALIDATION_FAILED"
    return state
