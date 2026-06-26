from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas import LoginRequest, LoginResponse, ProgramResponse
import crud

router = APIRouter(
    prefix="/api",
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):

    user = crud.get_user_by_hwid(
        db,
        request.hwid
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if user.active != 1:

        raise HTTPException(
            status_code=403,
            detail="User blocked"
        )

    programs = crud.get_user_programs(
        db,
        user.id
    )

    return LoginResponse(
        success=True,
        nickname=user.nickname,
        active=True,
        expire_date=user.expire_date,
        programs=[
            ProgramResponse(**p)
            for p in programs
        ]
    )