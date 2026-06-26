from pydantic import BaseModel
from typing import List


# =========================
# LOGIN
# =========================

class LoginRequest(BaseModel):
    hwid: str
    version: str = ""
    computer_name: str = ""
    windows: str = ""
    ip: str = ""


class ProgramResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    success: bool
    nickname: str
    active: bool
    expire_date: str
    programs: List[ProgramResponse]


# =========================
# REQUEST
# =========================

class CreateRequest(BaseModel):
    nickname: str
    hwid: str


# =========================
# HEARTBEAT
# =========================

class HeartbeatRequest(BaseModel):
    hwid: str
    program: str
    version: str
    ip: str