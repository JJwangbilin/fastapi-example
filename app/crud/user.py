from app.db.mongodb import AsyncIOMotorClient
from typing import Optional
from pydantic import EmailStr
from fastapi import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.core.config import database_name, user_collection_name
from app.models.user import UserInDB, UserInCreate
from app.common.security import generate_salt, get_password_hash, verify_password


async def get_user(conn: AsyncIOMotorClient, id: Optional[str] = None, username: Optional[str] = None,
                   email: Optional[str] = None, mobile: Optional[str] = None) -> UserInDB:
    if id:
        row = await conn[database_name][user_collection_name].find_one({"id": id})
        if row:
            return UserInDB(**row)
    if username:
        row = await conn[database_name][user_collection_name].find_one({"username": username})
        if row:
            return UserInDB(**row)
    if email:
        row = await conn[database_name][user_collection_name].find_one({"email": email})
        if row:
            return UserInDB(**row)
    if mobile:
        row = await conn[database_name][user_collection_name].find_one({"mobile": mobile})
        if row:
            return UserInDB(**row)


# 根据username,email,phone是否已存在
async def check_free_username_and_email_mobile(
        conn: AsyncIOMotorClient, username: Optional[str] = None, email: Optional[EmailStr] = None,
        mobile: Optional[str] = None
):
    if username:
        user_by_username = await get_user(conn, username=username)
        if user_by_username:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="用户名已被使用",
            )
    if email:
        user_by_email = await get_user(conn, email=email)
        if user_by_email:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="邮箱已被使用",
            )
    if mobile:
        user_by_mobile = await get_user(conn, mobile=mobile)
        if user_by_mobile:
            raise HTTPException(
                status_code=HTTP_422_UNPROCESSABLE_ENTITY,
                detail="手机号已被使用",
            )


async def create_user(conn: AsyncIOMotorClient, user: UserInCreate) -> UserInDB:
    salt = generate_salt()
    hashed_password = get_password_hash(salt + user.password)
    db_user = user.dict()
    db_user['salt'] = salt
    db_user['hashed_password'] = hashed_password
    del db_user['password']

    row = await conn[database_name][user_collection_name].insert_one(db_user)

    return UserInDB(**user.dict())
