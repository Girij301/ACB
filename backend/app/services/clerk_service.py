from clerk_backend_api import Clerk

from app.core.config import settings

clerk = Clerk(
    bearer_auth=settings.CLERK_SECRET_KEY,
)


class ClerkService:
    """
    Wrapper around the Clerk Backend SDK.
    """

    def get_user(
        self,
        clerk_user_id: str,
    ):
        return clerk.users.get(
            user_id=clerk_user_id,
        )
