

AGENT_CARD = {
    "id": "echo-agent-v1",
    "name": "Echo Agent",
    "version": "1.0.0",
    "description": "A simple agent that echoes back any text it receives.",
    "url": "http://localhost:8000", # updated at deploy time
    "contact": {
        "email": "support@example.com"
    },
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],

    "skills": [
        {
            "id": "echo",
            "name": "Echo",
            "description": "Returns the user message verbatim.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"]
        },
        {
            "id": "summarize",
            "name": "Summarize",
            "description": "Summarizes the user-provided text.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"],
        }
    ]
}

def validate_card(card: dict) -> bool:
    required_fields = {
        "id",
        "name",
        "version",
        "description",
        "url",
        "contact",
        "capabilities",
        "defaultInputModes",
        "defaultOutputModes",
        "skills",
    }

    if not isinstance(card, dict):
        return False

    if not required_fields.issubset(card.keys()):
        return False

    contact = card.get("contact")
    if not isinstance(contact, dict) or "email" not in contact:
        return False

    return True