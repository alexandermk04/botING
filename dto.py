from dataclasses import dataclass

@dataclass
class Message:
    content: str
    author: str

@dataclass
class Conversation:
    message: Message
    history: list[Message]