from fastapi import APIRouter
router = APIRouter(prefix="/users")

@router.get("/")
async def something():
    pass
