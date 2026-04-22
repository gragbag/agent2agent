import uuid
import asyncio

try:
    from .agent_card import AGENT_CARD
    from .handlers import handle_task
except ImportError:
    from agent_card import AGENT_CARD
    from handlers import handle_task


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
        # Called once when the container starts.
        # Initialise models, DB connections, etc. here.
        print('EchoAgent.set_up() called')

    def query(
        self,
        *,
        task_id: str = None,
        session_id: str = None,
        message_text: str,
        metadata: dict | None = None,
    ) -> dict:
        """
        Agent Engine calls this method for each request.
        We mirror the A2A task send/receive pattern here.
        """
        from types import SimpleNamespace
        # Re-use the same handler logic as the HTTP server
        fake_request = SimpleNamespace(
            id=task_id or str(uuid.uuid4()),
            sessionId=session_id,
            metadata=metadata,
            message=SimpleNamespace(
                role='user',
                parts=[SimpleNamespace(type='text', text=message_text)]
            )
        )
        result_text = _run_async(handle_task(fake_request))
        return {
            'id': fake_request.id,
            'status': {'state': 'completed'},
            'artifacts': [{'parts': [{'type': 'text', 'text': result_text}]}],
        }

    def get_agent_card(self) -> dict:
        return AGENT_CARD


root_agent = EchoAgent()
