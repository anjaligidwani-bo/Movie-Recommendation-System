from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.validators.user import RegisterSchema, LoginSchema
from app.models import User, UserLogin
from app.repositories.create_user_repositories import CreateUserRepository
from app.core.security import create_access_token, decode_access_token, Hashing, Verify
from app.utils.validators import is_strong_password
from app.core.logging_config import logger
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES as ACCESS_EXPIRE_MINUTES


def register_user(payload: RegisterSchema, db: Session):
    repo = CreateUserRepository(db)

    existing = repo.get_user_by_email(payload.email)
    if existing:
        logger.warning(f"Attempt to register existing email: {payload.email}")
        raise HTTPException(400, "User already exists")

    if not is_strong_password(payload.password):
        raise HTTPException(400, "Weak password")

    hashed = Hashing(payload.password)
    user = User(
        username=payload.username,
        email=payload.email,
        password=hashed,
        role=payload.role.value,
    )

    repo.add_user(user)
    logger.info(f"User registered: {payload.email}")
    return {"message": "Registered", "user_id": user.id}


def login_user(payload: LoginSchema, db: Session):
    repo = CreateUserRepository(db)

    user = repo.get_user_by_email(payload.email)
    if not user or not Verify(payload.password, user.password):
        logger.warning(f"Login failed for {payload.email}")
        raise HTTPException(401, "Invalid credentials")

    token_data = {
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "user_id": user.id,
    }
    token = create_access_token(token_data, expire_minutes=ACCESS_EXPIRE_MINUTES)

    login = repo.get_user_login(user.id)
    if login:
        login.token = token
        login.status = "active"
        repo.update_user_login(login)
    else:
        login = UserLogin(user_id=user.id, token=token)
        repo.add_user_login(login)

    logger.info(f"User logged in: {payload.email}")
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_login_id": login.id,
        "role": user.role,
    }


def validate_token(token: str):
    payload = decode_access_token(token)
    if not payload:
        logger.warning("Invalid token validation attempt")
        raise HTTPException(401, "Invalid or missing token")
    return payload


def logout_user(user_login_id: int, db: Session):
    repo = CreateUserRepository(db)
    login = repo.deactivate_user_login(user_login_id)
    if not login:
        raise HTTPException(404, "Login not found")
    logger.info(f"User logout: {login.user_id}")
    return {"message": "Logged out"}
