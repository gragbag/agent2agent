from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import Any, Optional, Literal, Union

try:
    from .agent_card import AGENT_CARD, get_agent_card
    from .handlers import handle_task
except ImportError:
    from agent_card import AGENT_CARD, get_agent_card
    from handlers import handle_task

AGENT_NAME = "Echo Agent"

app = FastAPI(title=AGENT_NAME)

# ── Endpoint 1: Agent Card ──────────────────────────────────────────
@app.get('/.well-known/agent.json')
async def get_agent_card_endpoint(request: Request):
    base_url = str(request.base_url).rstrip("/")
    return get_agent_card(url=base_url or AGENT_CARD["url"])

@app.get('/health')
async def get_health():
    return {
        "status": "ok",
        "agent": AGENT_CARD["id"]
    }

# ── Pydantic models for the A2A task message schema ─────────────────
class TextPart(BaseModel):
    type: str = 'text'
    text: str

class FileObject(BaseModel):
    url: str
    mimeType: str


class FilePart(BaseModel):
    type: Literal["file"] = "file"
    file: FileObject

class Message(BaseModel):
    role: str # 'user' or 'agent'
    parts: list[Union[TextPart, FilePart]]

class TaskRequest(BaseModel):
    id: str # client-generated task ID
    sessionId: Optional[str] = None
    message: Message
    metadata: Optional[dict[str, Any]] = None

# ── Endpoint 2: Send Task ────────────────────────────────────────────
@app.post('/tasks/send')
async def send_task(request: TaskRequest):
    if not request.message.parts:
        raise HTTPException(status_code=400, detail="message.parts cannot be empty")
    
    result_text = await handle_task(request)
    return {
        'id': request.id,
        'status': {'state': 'completed', "message": None},
        'artifacts': [
            {
                'parts': [{'type': 'text', 'text': result_text}]
            }
        ]
    }
