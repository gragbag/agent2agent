async def handle_task(request) -> str:
    text_parts = [p.text for p in request.message.parts if p.type == "text"]
    combined = " ".join(text_parts).strip()
    if not combined:
        return ""

    words = combined.split()
    return " ".join(reversed(words))

