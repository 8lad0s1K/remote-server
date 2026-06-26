from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import crud

router = APIRouter(
    prefix="/api",
    tags=["Programs"]
)


@router.get("/programs/{hwid}")
def get_programs(
    hwid: str,
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_hwid(db, hwid)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return crud.get_user_programs(
        db,
        user.id
    )