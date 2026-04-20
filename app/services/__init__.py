# from fastapi import APIRouter

# from .movies import router as movies_router
# from .halls import router as halls_router
# from .movie_sessions import router as movie_sessions_router
# from .users import router as users_router
# router = APIRouter()

# router.include_router(movies_router)
# router.include_router(halls_router)
# router.include_router(movie_sessions_router)
# router.include_router(users_router)
from .user_service import get_user_by_email, create_user

from .hall_service import add_hall

from .movie_service import (
    add_movie,
    get_all_movies,
    get_movie_by_id,
    delete_movie,
)

from .movie_session_service import (
    add_movie_session,
    get_all_movie_sessions
)