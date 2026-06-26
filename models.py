from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import relationship

from database import Base


# =========================
# USERS
# =========================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    hwid = Column(String, unique=True, index=True)

    active = Column(Integer, default=1)

    nickname = Column(String)

    expire_date = Column(String)

    programs = relationship(
        "UserProgram",
        back_populates="user",
        cascade="all, delete-orphan"
    )


# =========================
# PROGRAMS
# =========================

class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String)

    users = relationship(
        "UserProgram",
        back_populates="program"
    )


# =========================
# USER PROGRAMS
# =========================

class UserProgram(Base):
    __tablename__ = "user_programs"

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True
    )

    program_id = Column(
        Integer,
        ForeignKey("programs.id"),
        primary_key=True
    )

    active = Column(Integer, default=1)

    user = relationship(
        "User",
        back_populates="programs"
    )

    program = relationship(
        "Program",
        back_populates="users"
    )


# =========================
# PENDING REQUESTS
# =========================

class PendingRequest(Base):
    __tablename__ = "pending_requests"

    id = Column(Integer, primary_key=True, index=True)

    nickname = Column(String)

    hwid = Column(String)

    created_at = Column(DateTime)