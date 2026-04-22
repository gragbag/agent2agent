AGENT_ID = "reverse-agent-v1"
AGENT_NAME = "Reverse Agent"
AGENT_VERSION = "1.0.0"
AGENT_DESCRIPTION = "An A2A-compatible agent that returns the user's words in reverse order."
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
            "id": "reverse",
            "name": "Reverse",
            "description": "Returns the user's words in reverse order.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"],
        }
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

