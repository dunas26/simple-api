from fastapi import APIRouter
from v1.endpoints.models import Signup

router = APIRouter(tags=["auth"])


@router.post("/signup")
def signup_request(signup: Signup):
    """Responds to a signup request."""
    return {"msg": "Sign up ok"}
