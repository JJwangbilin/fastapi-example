from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.core.jwt import get_current_user_authorizer
from app.core import config
from app.models.user import UserInResponse, User
from loguru import logger

router = APIRouter()


@router.get("/me", response_model=UserInResponse, tags=['user'], name="用户信息")
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer())):
    logger.info(user)
    return UserInResponse(user=user)


@router.get("/test", tags=['user'], name="用户信息可选")
async def retrieve_current_user(user: User = Depends(get_current_user_authorizer(required=False))):
    logger.info(user)
    return {}
