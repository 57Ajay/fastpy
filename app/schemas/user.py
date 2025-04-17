from pydantic import BaseModel, EmailStr, ConfigDict

class UserCreate(BaseModel):

    username: str
    email: EmailStr | None = None
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
    )

class UserInDBBase(BaseModel):

    id: int
    username: str
    email: EmailStr | None = None
    is_active: bool = True
    model_config = ConfigDict(
        from_attributes=True )


class UserPublic(UserInDBBase):
    pass

class UserInDB(UserInDBBase):
     hashed_password: str
 
