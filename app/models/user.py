from pydantic import BaseModel, UUID1, EmailStr, HttpUrl, Field
from app.models.common import IDModel, CreatedAtModel, UpdatedAtModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

from app.common.security import generate_salt, get_password_hash, verify_password


class _ChannelEnum(str, Enum):
    RG = '注册'
    WX = '微信'
    QQ = 'QQ'
    GIT = 'GitHub'


class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    mobile: str = Field(None, regex='^1[3456789]\d{9}$')
    unionid: str = Field(None, title='三方登录唯一id')
    channel: _ChannelEnum
    role: List[int]
    remark: str = None
    thumb: HttpUrl
    activated: bool


class User(UserBase):
    token: str


class UserInDB(UserBase):
    id: str = ""
    salt: str = ""
    hashed_password: str = ""
    updatedAt: datetime
    createdAt: datetime

    def check_password(self, password: str):
        return verify_password(self.salt + password, self.hashed_password)


class UserInResponse(BaseModel):
    user: User


# 写入数据库，和前端请求参数无关
class UserInCreate(UserBase, IDModel, CreatedAtModel, UpdatedAtModel):
    password: str


class UserInLogin(BaseModel):
    name: str = Field(..., title="手机号/邮箱")
    password: str


class _StatusEnum(str, Enum):
    A = '待审核'
    E = '审核通过'
    F = '审核未通过'


class UserExtInDB(BaseModel):
    id: UUID1
    professional: str = None
    desc: str = None
    status: _StatusEnum
    reason: str = None
    percent: float
    realname: str = None
    bank_no: str = None
    bank_name: str = None
