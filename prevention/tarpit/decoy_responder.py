"""
Decoy & Tarpit Module for ARTEX Swarm Neutralization.
Provides fake API endpoints and 'fake wins' to trap autonomous agent worker loops.
"""

from typing import Dict, Any
import json
import time


def evaluate_and_tarpit(request_payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Detects if an incoming request exhibits autonomous agent characteristics
    (e.g., suspicious User-Agent like Playwright/Norma SDK or high-frequency scanning)
    and returns a convincing 'fake win' response to stall the agent loop.
    """
    user_agent = request_payload.get("user_agent", "")
    suspicious_agents = ["playwright", "normasdk", "python-requests", "wget", "curl"]
    
    is_suspicious = any(agent in user_agent.lower() for agent in suspicious_agents)
    
    if is_suspicious:
        # Introduce intentional LLM-pacing latency to drain actor compute budget
        time.sleep(2.5)
        
        return {
            "status_code": 200,
            "tarpit_engaged": True,
            "response_body": json.dumps({
                "status": "success",
                "message": "Access granted to administrative staging root.",
                "fake_flag": "FLAG{artex_tarpit_decoy_success_9912}"
            }),
            "log_note": "Decoy tarpit engaged: fed fake win response to consume agent budget."
        }
    
    return {
        "status_code": 403,
        "tarpit_engaged": False,
        "response_body": "Access Denied."
    }