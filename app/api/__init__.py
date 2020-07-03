from fastapi import APIRouter

from app.api.authenticaion import router as auth_router
router = APIRouter()
'''
example:
    router.include_router(xxx, tags=["xxx"], prefix="/xxx")
'''
router.include_router(auth_router)