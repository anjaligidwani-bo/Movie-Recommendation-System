from sqlalchemy.orm import Session
from app.models import Movies, Watchlist
from fastapi import HTTPException
from app.core.logging_config import logger
from sqlalchemy import func
from typing import Optional
from app.repositories.user_repository import UserRepository

# --------------------- WATCHLIST --------------------- #


def add_to_watchlist(db, user_id: int, movie_ids: list[int], status: str = "To Watch"):
    repo = UserRepository(db)
    added = []

    for movie_id in movie_ids:
        exists = repo.get_watchlist_entry(user_id, movie_id)
        if exists:
            continue

        movie = repo.get_movie_by_id(movie_id)
        if not movie:
            raise HTTPException(404, f"Movie with ID {movie_id} not found")

        entry = Watchlist(
            user_id=user_id, movie_id=movie_id, movie_title=movie.title, status=status
        )
        repo.add_watchlist_entry(entry)
        added.append({"movie_id": movie_id, "title": movie.title})

    logger.info(f"Movie {added} added to watchlist by user {user_id} with status {status}")
    
    return {"added_movies": added, "status": status}


def update_watchlist_status(db, user_id: int, movie_id: int, status: str):
    repo = UserRepository(db)
    entry = repo.get_watchlist_entry(user_id, movie_id)
    if not entry:
        raise HTTPException(404, "Movie not in Watchlist")
    entry.status = status
    repo.update_watchlist_entry(entry)
    logger.info(f"User {user_id} updated movie {movie_id} status to {status}")
    return {"movie_id": movie_id, "status": status}


def list_watchlist(db, user_id: int, status=None, sort="created_at", order="desc", page=1, size=10):
    repo = UserRepository(db)
    results = repo.list_watchlist(user_id, status, sort, order, page, size)
    return [
        {
            "movie_id": w.Watchlist.movie_id,
            "title": w.Watchlist.movie_title,
            "status": w.Watchlist.status,
            "added_at": w.Watchlist.created_at,
        }
        for w in results
    ]


def remove_from_watchlist(db, user_id: int, movie_id: int):
    repo = UserRepository(db)
    entry = repo.get_watchlist_entry(user_id, movie_id)
    if not entry:
        raise HTTPException(404, "Movie not in watchlist")
    repo.delete_watchlist_entry(entry)
    logger.info(f"Movie {movie_id} removed from watchlist by user {user_id}")
    return {"removed_movie": movie_id}


def remove_bulk_watchlist(db, user_id: int, movie_ids: list[int]):
    repo = UserRepository(db)
    repo.delete_bulk_watchlist(user_id, movie_ids)
    logger.info(f"Movies {movie_ids} removed from watchlist by user {user_id}")
    return {"removed_movies": movie_ids}


def check_in_watchlist(db, user_id: int, movie_id: int):
    repo = UserRepository(db)
    entry = repo.get_watchlist_entry(user_id, movie_id)
    if not entry:
        return {"inWatchlist": False}
    return {"inWatchlist": True, "status": entry.status}

def watchlist_status(db, user_id: int, status:str):

    repo = UserRepository(db)
    count = repo.movie_count(user_id, status)
    return {"status": status, "count": count}


def search_movies(db, q=None, genre=None, page=1, limit=10, sort_by="rating", order="desc"):
    repo = UserRepository(db)
    return repo.search_movies(q, genre, page, limit, sort_by, order)
