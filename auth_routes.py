from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.create_user import (
    register_user,
    login_user,
    logout_user,
    validate_token,
)
from app.validators.user import RegisterSchema, LoginSchema
from app.db.session import get_db
from app.core.security import decode_access_token
from app.core.logging_config import logger


auth = APIRouter(tags=["Authentication"])
bearer_scheme = HTTPBearer()


# ---------------- User/Admin Registration ---------------- #
@auth.post("/register")
def register_users(user: RegisterSchema, db: Session = Depends(get_db)):
    # Register a new user (Admin can create users)
    try:
        result = register_user(user, db)
        logger.info(f"User registration attempted for {user.email}")
        return result
    except Exception as e:
        logger.error(f"User registration failed for {user.email}: {e}")
        raise HTTPException(500, "Internal Server Error")


# ---------------- Login ---------------- #
@auth.post("/login")
def login_users(payload: LoginSchema, db: Session = Depends(get_db)):
    # Login user and return JWT token

    result = login_user(payload, db)
    logger.info(f"User login attempt: {payload.email}")
    return result

# ---------------- Validate Token ---------------- #

@auth.post("/validate_token")
def validate_tokens(cred: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # Validate JWT token and return user info

    token = cred.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(401, "Invalid or missing token")
    return {
        "user_id": payload["user_id"],
        "email": payload["email"],
        "role": payload["role"],
    }


# ---------------- Logout ---------------- #
@auth.post("/logout")
def logout_users(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Logout user by invalidating JWT token

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    result = logout_user(payload["user_id"], db)
    logger.info(f"User logout: {payload['email']}")
    return result
