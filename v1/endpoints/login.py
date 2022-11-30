from fastapi import APIRouter, Depends, HTTPException, status
from core.schemas.responses import TokenResponse, APIResponse
from core.repositories import UserRepository
from core.services.auth import HashService, TokenGenerationService
from core.dependencies import user_repository, hash_service, token_generation_service
from .models import Login

router = APIRouter(tags=["auth"])


@router.post(
    "/login", response_model=TokenResponse, responses={404: {"model": APIResponse}}
)
def login_request(
    login: Login,
    user_repository: UserRepository = Depends(user_repository),
    hash_service: HashService = Depends(hash_service),
    token_generation_service: TokenGenerationService = Depends(
        token_generation_service
    ),
):
    """Logs any user with a valid username and password"""
    user = user_repository.get_by_username(login.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User "{login.username}" was not found',
        )

    if not hash_service.match_password(login.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid credentials"
        )

    token = token_generation_service.generate_access_token(user.username)
    refresh_token = token_generation_service.generate_refresh_token(user.username)

    return {
        "msg": f"Login successful: {user.username if user else 'Not found'}",
        "token": token,
        "refresh_token": refresh_token,
    }
