from sqlalchemy.orm import Session

from models import (
    User,
    Program,
    UserProgram,
    PendingRequest
)


# =====================================
# USERS
# =====================================

def get_user_by_hwid(db: Session, hwid: str):
    return (
        db.query(User)
        .filter(User.hwid == hwid)
        .first()
    )


def get_user_by_id(db: Session, user_id: int):
    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_all_users(db: Session):
    return (
        db.query(User)
        .order_by(User.id)
        .all()
    )


# =====================================
# PROGRAMS
# =====================================

def get_programs(db: Session):
    return (
        db.query(Program)
        .order_by(Program.id)
        .all()
    )


def get_user_programs(db: Session, user_id: int):

    rows = (
        db.query(UserProgram)
        .filter(UserProgram.user_id == user_id)
        .all()
    )

    result = []

    for row in rows:

        program = (
            db.query(Program)
            .filter(Program.id == row.program_id)
            .first()
        )

        if program and row.active == 1:

            result.append(
                {
                    "id": program.id,
                    "name": program.name
                }
            )

    return result


# =====================================
# REQUESTS
# =====================================

def request_exists(db: Session, hwid: str):

    return (
        db.query(PendingRequest)
        .filter(PendingRequest.hwid == hwid)
        .first()
    )


def create_request(
    db: Session,
    nickname: str,
    hwid: str
):

    exists = request_exists(db, hwid)

    if exists:
        return exists

    request = PendingRequest(
        nickname=nickname,
        hwid=hwid
    )

    db.add(request)
    db.commit()
    db.refresh(request)

    return request


def get_pending_requests(db: Session):

    return (
        db.query(PendingRequest)
        .order_by(PendingRequest.id)
        .all()
    )