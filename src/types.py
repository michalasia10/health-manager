from dataclasses import dataclass
from urllib.request import Request


@dataclass
class User:
    id: int
    role: str
    is_anonymous: bool


class RRequest(Request):
    user: User
