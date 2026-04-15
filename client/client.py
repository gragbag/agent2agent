import uuid
from typing import Any, Optional

import httpx


class A2AClient:
    """Minimal A2A-compliant client."""

    def __init__(self, agent_url: str):
        self.agent_url = agent_url.rstrip("/")
        self._card: Optional[dict[str, Any]] = None
        self._http = httpx.Client(timeout=30)

    # ── 1. Discovery ─────────────────────────────────────────────────
    def fetch_agent_card(self) -> dict[str, Any]:
        """Fetch and cache the Agent Card."""
        if self._card is None:
            url = f"{self.agent_url}/.well-known/agent.json"
            resp = self._http.get(url)
            resp.raise_for_status()
            self._card = resp.json()
        return self._card

    def get_skills(self) -> list[dict[str, Any]]:
        """Return the skills list from the cached Agent Card."""
        card = self.fetch_agent_card()
        return card.get("skills", [])

    # ── 2. Request Construction ──────────────────────────────────────
    def _build_task(
        self,
        text: str,
        task_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> dict[str, Any]:
        """Build a conformant A2A task payload."""
        return {
            "id": task_id or str(uuid.uuid4()),
            "sessionId": session_id,
            "message": {
                "role": "user",
                "parts": [{"type": "text", "text": text}],
            },
        }

    # ── 3. Send & Parse ──────────────────────────────────────────────
    def send_task(self, text: str, **kwargs) -> dict[str, Any]:
        """Send a task and return the parsed response."""
        self.fetch_agent_card()  # ensure card is cached
        payload = self._build_task(text, **kwargs)
        url = f"{self.agent_url}/tasks/send"
        resp = self._http.post(url, json=payload)
        resp.raise_for_status()

        data = resp.json()
        state = data.get("status", {}).get("state")
        if state != "completed":
            raise RuntimeError(f"Task did not complete successfully. status.state={state!r}")

        return data

    # ── 4. Helper: extract result text ───────────────────────────────
    @staticmethod
    def extract_text(response: dict[str, Any]) -> str:
        """Pull the first text part from artifacts."""
        artifacts = response.get("artifacts", [])
        for artifact in artifacts:
            for part in artifact.get("parts", []):
                if part.get("type") == "text":
                    return part.get("text", "")
                if part.get("type") == "file":
                    return part.get("file", {}).get("url", "")
        return ""

    # ── 5. Resource cleanup / context manager ────────────────────────
    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> "A2AClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()