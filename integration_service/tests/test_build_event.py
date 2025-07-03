import pytest
from src.services.event_builder import EventBuilder


def test_build_event_from_telegram():
    body = {
        "message": {
            "chat": {"id": 123},
            "from": {"id": 456, "username": "user1"},
            "message_id": 789,
            "text": "Hello"
        }
    }

    event = EventBuilder.build_event_from_telegram(body)
    assert event is not None
    assert event["event_type"] == "telegram.message_received"
    assert event["data"]["text"] == "Hello"
    assert event["data"]["chat_id"] == 123
