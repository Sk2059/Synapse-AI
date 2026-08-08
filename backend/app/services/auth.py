from fastapi import  HTTPException, status
from app.core.security import verify_password, create_access_token, hash_password

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest

class AuthService:
    def __init__(self,user_repository:UserRepository):
        self.user_repository = user_repository

    async def register_user(self,data:RegisterRequest)-> User:
        existing_user = await self.user_repository.get_by_email(
            data.email
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        hashed_password = hash_password(data.password)
        user = User(
            email=data.email,
            username=data.username,
            hashed_password=hashed_password
        )
        return await self.user_repository.create(user)

    async def login(
            self,
            email: str,
            password: str,
        ) -> str:

            user = await self.user_repository.get_by_email(email)

            if not user or not verify_password(
                password,
                user.hashed_password,
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials",
                )

            return create_access_token(str(user.id))