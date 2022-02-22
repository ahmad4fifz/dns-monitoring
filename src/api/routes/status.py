from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_description="Status retrieved from dependencies!")
async def get_status():
    return {"message": "Status"}
