from app.core.schemas import SyncModelORM
from app.users.models import Role, Gender, AddressType
from datetime import datetime
from pydantic import EmailStr, computed_field

class UserSchema(SyncModelORM):
    id: int
    name: str
    surname: str
    email: EmailStr
    gender: Gender
    birth_date: datetime | None
    role: Role
    addresses: list[AddressSchema]
    telephone_number: str | None
    created_at: datetime
    last_seen_at: datetime
    is_active: bool
    

class UserCreateSchema(SyncModelORM):
    name: str
    surname: str
    email: EmailStr
    password: str
    

class AddressSchema(SyncModelORM):
    id: int
    type: AddressType
    via: str
    city: str
    cap: str
    province: str
    country: str
    delivery_annotation: str
    default: bool
    user_id: int
    

class UserReviewResponseSchema(SyncModelORM):
    id: int
    name: str
    surname: str
    
    # add extra field calculated in serializer
    @computed_field
    @property
    def name_surname(self) -> str:
        return f"{self.name} {self.surname[0].capitalize()}."