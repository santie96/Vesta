from fastapi import APIRouter, Depends, status, Query
from app.database.connection import get_db, AsyncSession
from .schemas import *
from .services import *
from app.core.exceptions.exception_handlers import limiter


router = APIRouter(
    prefix="/auth",
    tags=["User Authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    return await create_user_service(payload, db, False)