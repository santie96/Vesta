from .schemas import *
from .exceptions import *
from app.database.connection import AsyncSession
from app.users.models import User, Address
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from .pwd import create_password_hash


async def get_user_by_id(user_id: int, db: AsyncSession) -> User:
    """
    Get user by id if exists
    """
    
    user = (
        await db.execute(
            select(User).where(User.id == user_id)
        )
    ).scalar_one_or_none()
    
    if not user:
        raise UserNotFoundException(f"User with id {user_id} not found")
    
    return user


async def get_user_by_email(email: str, db: AsyncSession) -> User | None:
    """
    Get user by email if exists
    """
    
    user = (
        await db.execute(
            select(User).where(User.email == email)
        )
    ).scalar_one_or_none()
    
    return user


async def create_user_service(payload: UserCreateSchema, db: AsyncSession, is_admin: bool) -> UserSchema:
    """
    Create a new user
    """
    
    existing_user = await get_user_by_email(payload.email, db)
    
    if existing_user is not None:
        raise UserAlreadyExistsException(f"User with email {payload.email} already exists")
    
    user = User(
        name=payload.name,
        surname=payload.surname,
        email=payload.email,
        hash_pwd=create_password_hash(payload.password),
        role=Role.ADMIN if is_admin else Role.USER,
    )
    
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    new_user = (
        await db.execute(
            select(User)
            .where(User.email == payload.email)
            .options(selectinload(User.addresses))   
        )        
    ).scalar_one()
    
    return UserSchema.model_validate(new_user)