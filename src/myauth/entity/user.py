from dataclasses import dataclass

from src.core.entity import Entity


@dataclass
class UserEntity(Entity):
    id: str
    role: str
    is_anonymous: bool
