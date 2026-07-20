# verify req.
from clerk_backend_api import Clerk
from clerk_backend_api.security import AuthenticateRequestOptions, AuthStatus
from fastapi import HTTPException, Request, status

from app.core.config import settings

clerk = Clerk(
    bearer_auth=settings.CLERK_SECRET_KEY,
)


def verify_request(request: Request):
    """
    Verify the incoming Clerk session token.
    """
    state = clerk.authenticate_request(
        request,
        AuthenticateRequestOptions(
            secret_key=settings.CLERK_SECRET_KEY,
            authorized_parties=[
                origin.strip()
                for origin in settings.CLERK_AUTHORIZED_PARTIES.split(",")
            ],
        ),
    )

    if state.status != AuthStatus.SIGNED_IN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized",
        )

    return state
