from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from core.database import db_session
from core.repositories import UserRepository
from core.services.auth import HashService, TokenService, TokenGenerationService


def get_database() -> Generator[Session, None, None]:
    try:
        db: Session = db_session()
        yield db
    finally:
        db.close()


def user_repository(
    db: Session = Depends(get_database),
) -> Generator[UserRepository, None, None]:
    service = UserRepository(db)
    yield service


def hash_service() -> Generator[HashService, None, None]:
    service = HashService()
    yield service


def token_service() -> Generator[TokenService, None, None]:
    service = TokenService()
    yield service


def token_generation_service(
    token_srv=Depends(token_service),
) -> Generator[TokenGenerationService, None, None]:
    service = TokenGenerationService(token_srv)
    yield service
