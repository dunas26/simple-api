from sqlalchemy.orm import Session
from core.models import User


class ConnectionMixin:
    db: Session

    def __init__(self, db: Session):
        self.db = db


class UserRepository(ConnectionMixin):
    def __init__(self, db: Session):
        super().__init__(db)
        self.table: User = User

    def get_by_id(self, id: int) -> User:
        return self.db.query(self.table).filter_by(id=id).first()

    def get_by_username(self, username: str) -> User:
        return self.db.query(self.table).filter_by(username=username).first()

    def get_all(self) -> list[User]:
        return self.db.query(self.table).all()

    def add(self, user: User):
        return self.db.add(user)
