async def handle_task(request) -> str:
    text_parts = [p.text for p in request.message.parts if p.type =='text']
    combined = ' '.join(text_parts)

    if combined.startswith("!summarize"):
        return "This is a mock one-sentence summary of the provided text."
    
    # ECHO skill: return the input unchanged
    return combined