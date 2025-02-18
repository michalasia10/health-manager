from abc import ABC, abstractmethod


class AuthClient(ABC):
    @abstractmethod
    async def email_sign_up(
        self, email: str, password: str, first_name: str, last_name: str
    ) -> None:
        pass

    @abstractmethod
    async def email_login(self, email: str, password: str) -> None:
        pass

    @abstractmethod
    async def google_sign_up(self, redirect_url: str) -> None:
        pass
