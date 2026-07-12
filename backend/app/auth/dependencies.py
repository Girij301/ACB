from app.core.database import get_db
from app.repositories.user_repository import UserRepository
from app.services.clerk_service import ClerkService
from app.services.user_service import UserService
from fastapi import Depends
from sqlalchemy.orm import Session

from .clerk import verify_request


def get_current_user(
    state=Depends(verify_request),
    db: Session = Depends(get_db),
):
    payload = state.payload

    clerk_user_id = payload["sub"]

    clerk_user = ClerkService().get_user(clerk_user_id)

    primary_email = next(
        (
            email.email_address
            for email in clerk_user.email_addresses
            if email.id == clerk_user.primary_email_address_id
        ),
        None,
    )

    service = UserService(UserRepository(db))

    return service.sync_user(
        clerk_user_id=clerk_user.id,
        email=primary_email,
        first_name=clerk_user.first_name,
        last_name=clerk_user.last_name,
        image_url=clerk_user.image_url,
    )
