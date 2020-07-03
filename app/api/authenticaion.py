import time
from fastapi import APIRouter, Body, Depends
from starlette.exceptions import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST
from pydantic import EmailStr
from loguru import logger
from fastapi.security import OAuth2PasswordRequestForm

from app.db.mongodb import AsyncIOMotorClient, get_database
from app.core.jwt import create_access_token
from app.crud.user import create_user, check_free_username_and_email_mobile, get_user
from app.models.user import User, UserInCreate, UserInResponse, _ChannelEnum
from app.models.token import TokenResponse
from app.db.redis import Redis, get_redis_database

router = APIRouter()


@router.post("/users/login", response_model=TokenResponse, tags=["authentication"], name='邮箱/手机密码登录')
async def login(user: OAuth2PasswordRequestForm = Depends(), db: AsyncIOMotorClient = Depends(get_database)):
    dbuser = await get_user(db, email=user.username, mobile=user.username)
    if not dbuser or not dbuser.check_password(user.password):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="用户名或密码错误"
        )
    logger.info(dbuser.id)
    token = create_access_token(data={"id": dbuser.id})
    # swaggerui 要求返回此格式
    return TokenResponse(access_token=token)


@router.post("/users", response_model=UserInResponse, tags=["authentication"], name='邮箱注册')
async def register(email: EmailStr = Body(...), code: str = Body(...), password: str = Body(...),
                   db: AsyncIOMotorClient = Depends(get_database), rd: Redis = Depends(get_redis_database)):
    await check_free_username_and_email_mobile(db, email=email)
    # code 从redis校验邮箱验证码
    if code != rd.get(email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail="验证码错误"
        )
    # 组装默认参数，create_user只管insert
    user = UserInCreate(password=password,
                        username='moop{}'.format(int(time.time() * 1000)),
                        email=email,
                        channel=_ChannelEnum.RG,
                        role=[1],
                        thumb='https://www.baidu.com/img/flexible/logo/pc/result.png',
                        activated=True)
    dbuser = await create_user(db, user)
    token = create_access_token(data={"id": dbuser.id})

    return UserInResponse(user=User(**dbuser.dict(), token=token))
