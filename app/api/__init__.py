from fastapi import APIRouter

from app.api.authenticaion import router as auth_router
from app.api.user import router as user_router

router = APIRouter()
'''
example:
    router.include_router(xxx, tags=["xxx"], prefix="/xxx")
'''
router.include_router(auth_router)
router.include_router(user_router,prefix='/user')