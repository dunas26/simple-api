from fastapi import APIRouter, Depends
from v1.endpoints.models import Signup
from core.models import User
from core.repositories import UserRepository
from core.services.auth import HashService
from core.dependencies import user_repository, hash_service
from core.schemas.responses import DataResponse

router = APIRouter(tags=["auth"])


@router.post("/signup", response_model=DataResponse)
def signup_request(
    signup: Signup,
    user_repository: UserRepository = Depends(user_repository),
    hash_service: HashService = Depends(hash_service),
):
    """Responds to a signup request."""
    # Gather the data from the body
    username = signup.username
    email = signup.email
    # Hash the password using the hash service
    password = hash_service.hash_password(signup.password)
    # Add the user to the database
    user_repository.add(User(username=username, email=email, password=password))
    return {
        "msg": "User signup successful",
        "data": {"username": username, "email": email},
    }
