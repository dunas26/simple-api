from core.models import User


class MockUsersService:
    data: list[User]

    def __init__(self, test_data: list[User]):
        self.data = test_data

    def get_by_id(self, id: int) -> User:
        for d in self.data:
            if d.id == id:
                return d
        return None

    def get_by_username(self, username: str) -> User:
        for d in self.data:
            if d.username == username:
                return d
        return None

    def get_all(self) -> list[User]:
        return [x for x in self.data]

    def add(self, user: User):
        return self.data.append(user)
