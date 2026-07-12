from app.models.user import User
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(
        self,
        repository: UserRepository,
    ):
        self.repository = repository

    def sync_user(
        self,
        *,
        clerk_user_id: str,
        email: str,
        first_name: str | None = None,
        last_name: str | None = None,
        image_url: str | None = None,
    ) -> User:
        """
        Synchronize a Clerk user with the local database.

        - Create the user on first login.
        - Update profile information on subsequent logins.
        """

        user = self.repository.get_by_clerk_id(clerk_user_id)

        if user is None:
            return self.repository.create(
                clerk_user_id=clerk_user_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                image_url=image_url,
            )

        return self.repository.update(
            user,
            email=email,
            first_name=first_name,
            last_name=last_name,
            image_url=image_url,
        )
