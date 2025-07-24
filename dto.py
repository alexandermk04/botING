from dataclasses import dataclass

@dataclass
class Message:
    content: str
    author: str
    user_id: str | None = None

@dataclass
class Conversation:
    message: Message
    history: list[Message]