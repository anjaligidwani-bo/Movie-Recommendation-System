from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user_services import (
    search_movies,
    add_to_watchlist,
    list_watchlist,
    remove_from_watchlist,
    remove_bulk_watchlist,
    check_in_watchlist,
    update_watchlist_status,
    watchlist_status,
)
from app.validators.user import (
    SearchParams,
    WatchlistAdd,
)
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token, user_required
from app.core.logging_config import logger
from types import SimpleNamespace
from fastapi import HTTPException
from typing import List

user = APIRouter(tags=["User Operations"])
bearer_scheme = HTTPBearer()


# ---------------- Login Required ---------------- #


def require_login(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    # Dependency to ensure the user is logged in. Returns a SimpleNamespace with user_id, email, role.

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload:
        logger.warning("Unauthorized access attempt: invalid token")
        raise HTTPException(401, "Login required")

    role = payload.get("role")
    if not role or role.lower() != "user":
        logger.warning(
            f"Unauthorized access attempt by user {payload.get('email', 'unknown')}"
        )
        raise HTTPException(403, "User access required")

    return SimpleNamespace(
        user_id=payload.get("user_id"),
        email=payload.get("email"),
        role=payload.get("role"),
    )


# ---------------- Dashboard ---------------- #
@user.get("/dashboard")
@user_required
async def user_dashboard(
    request: Request, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
):
    """User Dashboard"""
    return {"message": f"Welcome user {request.state.user.email} to your dashboard!"}


# ---------------- Watchlist ---------------- #


@user.post("/watchlist")
@user_required
async def add_movie_to_watchlist(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    payload: WatchlistAdd = None,
    db: Session = Depends(get_db),
):
    user_id = request.state.user.user_id
    # Add movie(s) to watchlist
    if payload and payload.movie_ids:
        return add_to_watchlist(
            db=db,
            user_id=request.state.user.user_id,
            movie_ids=payload.movie_ids,
            status=payload.status,
        )
    return add_to_watchlist(
        db=db,
        user_id=request.state.user.user_id,
        movie_ids=payload.movie_ids,
        status="To Watch",
    )


@user.put("/watchlist/{movie_id}")
@user_required
async def update_watchlist(
    movie_id: int,
    status: str,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Update movie status
    return update_watchlist_status(
        db=db, user_id=request.state.user.user_id, movie_id=movie_id, status=status
    )


@user.get("/watchlist")
@user_required
async def get_users_watchlist(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    status: str = None,
    sort: str = "added_at",
    order: str = "desc",
    page: int = 1,
    size: int = 10,
    db: Session = Depends(get_db),
):
    # List all watchlist movies
    data = list_watchlist(
        db=db,
        user_id=request.state.user.user_id,
        status=status,
        sort=sort,
        order=order,
        page=page,
        size=size,
    )
    return data


@user.delete("/watchlist/{movie_id}")
@user_required
async def delete_watchlist_item(
    movie_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Remove a movie
    return remove_from_watchlist(
        db=db, user_id=request.state.user.user_id, movie_id=movie_id
    )


@user.delete("/watchlist")
# @user.delete("/watchlist/")
@user_required
async def delete_bulk_watchlist(
    movie_ids: List[int],
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Bulk Delete
    return remove_bulk_watchlist(
        db=db, user_id=request.state.user.user_id, movie_ids=movie_ids
    )


@user.get("/watchlist/{movie_id}/check")
@user_required
async def check_watchlist(
    movie_id: int,
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Check if movie is in watchlist
    return check_in_watchlist(
        db=db, user_id=request.state.user.user_id, movie_id=movie_id
    )


@user.get("/watchlist/summary")
@user_required
async def watchlist_status(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
):
    # Summary status
    return watchlist_status(db=db, user_id=request.state.user.user_id)


# ---------------- Movie Search ---------------- #
@user.post("/movies/search")
def movies_search(params: SearchParams, db: Session = Depends(get_db)):
    """Search movies"""
    return search_movies(
        db=db,
        q=params.q,
        genre=params.genre,
        page=params.page,
        limit=params.limit,
        sort_by=params.sort_by,
        order=params.order,
    )
