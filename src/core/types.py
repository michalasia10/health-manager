from urllib.request import Request


class RequestT(Request):
    from src.myauth.entity.user import UserEntity

    user: UserEntity
