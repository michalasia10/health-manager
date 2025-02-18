from ninja.router import Router

from src.myauth.dto import AuthSignupInputDto, AuthOutputDto
from src.myauth.service import AuthService

router = Router(tags=["auth"])

auth_service = AuthService()


@router.post("/signup", response=AuthOutputDto)
async def signup(request, data: AuthSignupInputDto):
    return await auth_service.sign_up(dto=data)


@router.post("/login", response=AuthOutputDto)
async def login(request, data: AuthSignupInputDto):
    return await auth_service.login(dto=data)
