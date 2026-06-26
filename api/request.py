from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas import CreateRequest
import crud

router = APIRouter(
    prefix="/api",
    tags=["Requests"]
)


@router.post("/request")
def create_request(
    request: CreateRequest,
    db: Session = Depends(get_db)
):
    crud.create_request(
        db,
        request.nickname,
        request.hwid
    )

    return {
        "success": True,
        "message": "Заявку подано."
    }