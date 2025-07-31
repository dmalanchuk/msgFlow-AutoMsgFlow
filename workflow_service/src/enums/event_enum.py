from enum import Enum


class EventType(str, Enum):
    NEW_MESSAGE = "message"
    EDITED_MESSAGE = "edited_message"
    NEW_MEMBER = "new_chat_member"
    LEFT_MEMBER = "left_chat_member"
    PHOTO = "photo"
    UNKNOWN = "unknown"
