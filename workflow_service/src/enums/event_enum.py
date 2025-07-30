from enum import Enum


class EventType(str, Enum):
    NEW_MEMBER = "new_chat_member"
    LEFT_MEMBER = "left_chat_member"
    PHOTO = "photo"
    UNKNOWN = "unknown"
