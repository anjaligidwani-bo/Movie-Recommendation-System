from fastapi import FastAPI
from app.middlewares.auth_middleware import AttachUserMiddleware
from app.api.v1 import auth_routes, user_watchlist_routes
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Movie Recommendation API",
    description="Movie recommendation system with Admin and User roles",
    version="1.0.0",
)

# Add middleware to attach user from JWT
app.add_middleware(AttachUserMiddleware)

# Enable CORS for Swagger/Postman
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_routes.auth, prefix="/auth")
app.include_router(user_watchlist_routes.user, prefix="/user")

@app.get("/")
def root():
    return {"message": "Welcome to Movie Recommendation API"}
