async def evaluate_conditions(conditions: dict, data: dict) -> bool:
    if "text_contains" in conditions:
        return conditions["text_contains"].lower() in data.get("text", "").lower()
    if "caption_contains" in conditions:
        return conditions["caption_contains"].lower() in data.get("caption", "").lower()
    return False
