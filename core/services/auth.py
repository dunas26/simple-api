from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from core.environment import jwt_environment


class HashService:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, pwd: str) -> str:
        return self.context.hash(pwd)

    def match_password(self, pwd: str, hashed_pwd: str) -> bool:
        return self.context.verify(pwd, hashed_pwd)


class TokenService:
    def encrypt(
        self,
        payload: dict,
        subject="app_auth",
        expiresIn: int = -1,
        secret: str = jwt_environment.SECRET,
    ) -> str:
        expiration_time = datetime.utcnow() + timedelta(
            seconds=expiresIn if expiresIn != -1 else 300
        )
        to_encode = {"exp": expiration_time, "sub": str(subject), "payload": payload}
        return jwt.encode(to_encode, secret, jwt_environment.ALGORITHM)

    def decrypt(
        self, token: str, secret: str = jwt_environment.SECRET, typing=None
    ) -> dict:
        token = jwt.decode(token, secret, algorithms=[jwt_environment.ALGORITHM])
        return typing(**token) if typing else token


class TokenGenerationService:
    def __init__(self, token_service: TokenService):
        self.token_service = TokenService()

    def generate_refresh_token(self, username: str):
        return self.token_service.encrypt(
            payload={"username": username},
            subject="refresh",
            expiresIn=jwt_environment.REFRESH_SECONDS,
            secret=jwt_environment.REFRESH_KEY,
        )

    def generate_access_token(self, username: str):
        return self.token_service.encrypt(
            payload={"username": username},
            subject="access",
            expiresIn=jwt_environment.SECRET_SECONDS,
            secret=jwt_environment.SECRET,
        )
