from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_clerk_id(
        self,
        clerk_user_id: str,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.clerk_user_id == clerk_user_id)
            .first()
        )

    def get_by_email(
        self,
        email: str,
    ) -> User | None:
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def create(
        self,
        *,
        clerk_user_id: str,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        image_url: str | None = None,
    ) -> User:
        user = User(
            clerk_user_id=clerk_user_id,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user

    def update(
        self,
        user: User,
        *,
        email: str,
        first_name: str | None,
        last_name: str | None,
        image_url: str | None,
    ) -> User:
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url

        self.db.commit()
        self.db.refresh(user)

        return user