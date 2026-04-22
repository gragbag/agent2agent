AGENT_ID = "echo-agent-v1"
AGENT_NAME = "Echo Agent"
AGENT_VERSION = "1.0.0"
AGENT_DESCRIPTION = "A simple A2A-compatible agent that echoes text and can mock summarize input."
AGENT_URL = "http://localhost:8080"
AGENT_CONTACT_EMAIL = "support@example.com"


_BASE_AGENT_CARD = {
    "id": AGENT_ID,
    "name": AGENT_NAME,
    "version": AGENT_VERSION,
    "description": AGENT_DESCRIPTION,
    "url": AGENT_URL,
    "contact": {
        "email": AGENT_CONTACT_EMAIL,
    },
    "capabilities": {
        "streaming": False,
        "pushNotifications": False,
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "skills": [
        {
            "id": "echo",
            "name": "Echo",
            "description": "Returns the user message verbatim.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"],
        },
        {
            "id": "summarize",
            "name": "Summarize",
            "description": "Summarizes the user-provided text.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"],
        },
    ],
}


def get_agent_card(*, url: str | None = None) -> dict:
    card = dict(_BASE_AGENT_CARD)
    card["contact"] = dict(_BASE_AGENT_CARD["contact"])
    card["capabilities"] = dict(_BASE_AGENT_CARD["capabilities"])
    card["defaultInputModes"] = list(_BASE_AGENT_CARD["defaultInputModes"])
    card["defaultOutputModes"] = list(_BASE_AGENT_CARD["defaultOutputModes"])
    card["skills"] = [dict(skill) for skill in _BASE_AGENT_CARD["skills"]]
    if url:
        card["url"] = url.rstrip("/")
    return card


AGENT_CARD = get_agent_card()
