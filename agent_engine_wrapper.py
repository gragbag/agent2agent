import asyncio
import uuid

AGENT_CARD = {
    "id": "echo-agent-v1",
    "name": "Echo Agent",
    "version": "1.0.0",
    "description": "A simple A2A-compatible agent that echoes text and can mock summarize input.",
    "url": "http://localhost:8080",
    "contact": {"email": "support@example.com"},
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


async def handle_task(request) -> str:
    text_parts = [p.text for p in request.message.parts if p.type == "text"]
    combined = " ".join(text_parts)

    if combined.startswith("!summarize"):
        return "This is a mock one-sentence summary of the provided text."

    return combined


def _run_async(coro):
    try:
        return asyncio.run(coro)
    except RuntimeError:
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()


class EchoAgent:
    """Agent Engine wrapper for the Echo A2A Agent."""

    def set_up(self):
        print("EchoAgent.set_up() called")

    def query(
        self,
        *,
        task_id: str = None,
        session_id: str = None,
        message_text: str,
        metadata: dict | None = None,
    ) -> dict:
        from types import SimpleNamespace

        fake_request = SimpleNamespace(
            id=task_id or str(uuid.uuid4()),
            sessionId=session_id,
            metadata=metadata,
            message=SimpleNamespace(
                role="user",
                parts=[SimpleNamespace(type="text", text=message_text)],
            ),
        )
        result_text = _run_async(handle_task(fake_request))
        return {
            "id": fake_request.id,
            "status": {"state": "completed"},
            "artifacts": [{"parts": [{"type": "text", "text": result_text}]}],
        }

    def get_agent_card(self) -> dict:
        return AGENT_CARD


root_agent = EchoAgent()
