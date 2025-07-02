class EventBuilder:

    @staticmethod
    def build_event_from_telegram(body: dict) -> dict | None:
        if "message" not in body:
            return {"status": None}

        msg = body["message"]
        chat = msg.get("chat", {})
        user = msg.get("from", {})

        base = {
            "chat_id": chat.get("id"),
            "user_id": user.get("id"),
            "message_id": msg.get("message_id"),
            "username": user.get("username", "")
        }

        if "text" in msg:
            return {
                "event_type": "telegram.message_received",
                "source": "telegram",
                "data": {**base, "text": msg["text"]}
            }

        if "photo" in msg:
            return {
                "event_type": "telegram.photo_received",
                "source": "telegram",
                "data": {**base, "caption": msg.get("caption", "")}
            }

        return {"status": None}
