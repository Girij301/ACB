from fastapi import APIRouter, Depends

from app.auth import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/me",
    tags=["User"],
)


@router.get("")
def me(
    current_user: User = Depends(get_current_user),
):
    """
    Returns the authenticated user from the local database.
    """

    return {
        "id": current_user.id,
        "clerk_user_id": current_user.clerk_user_id,
        "email": current_user.email,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "image_url": current_user.image_url,
    }