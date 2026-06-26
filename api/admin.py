from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from database import get_db
import crud

router = APIRouter(prefix="/api/admin", tags=["Admin Operations"])

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(get_db)):
    # Використовуємо існуючі або прості агрегації з crud
    import models
    return {
        "total_users": db.query(models.User).count(),
        "active_users": db.query(models.User).filter(models.User.active == True).count(),
        "blocked_users": db.query(models.User).filter(models.User.active == False).count(),
        "pending_requests": db.query(models.PendingRequest).count(),
        "issued_programs": db.query(models.UserProgram).count(),
        "active_licenses": db.query(models.User).filter(models.User.active == True).count(), 
    }

@router.get("/requests")
def list_requests(db: Session = Depends(get_db)):
    import models
    requests = db.query(models.PendingRequest).order_by(models.PendingRequest.id.desc()).all()
    return [{"id": r.id, "nickname": r.nickname, "hwid": r.hwid, "created_at": str(r.created_at)} for r in requests]

@router.post("/requests/{request_id}/approve")
def approve_request(request_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    # Логіка схвалення: створення користувача або оновлення, видача ліцензій
    import models
    req = db.query(models.PendingRequest).filter(models.PendingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Заявку не знайдено")
    
    # Визначаємо термін ліцензії
    days = data.get("days")
    import datetime
    expire_date = "LIFETIME" if days is None else (datetime.date.today() + datetime.timedelta(days=int(days))).strftime("%Y-%m-%d")
    
    user = db.query(models.User).filter(models.User.hwid == req.hwid).first()
    if not user:
        user = models.User(nickname=req.nickname, hwid=req.hwid, active=True, expire_date=expire_date)
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.nickname = req.nickname
        user.active = True
        user.expire_date = expire_date
        db.commit()

    # Програми
    program_states = data.get("program_states", {})
    db.query(models.UserProgram).filter(models.UserProgram.user_id == user.id).delete()
    for p_id, is_active in program_states.items():
        if is_active:
            up = models.UserProgram(user_id=user.id, program_id=int(p_id), active=1)
            db.add(up)
    
    db.delete(req)
    db.commit()
    return {"success": True}

@router.post("/requests/{request_id}/reject")
def reject_request(request_id: int, db: Session = Depends(get_db)):
    import models
    req = db.query(models.PendingRequest).filter(models.PendingRequest.id == request_id).first()
    if not req:
        raise HTTPException(status_code=404, detail="Заявку не знайдено")
    db.delete(req)
    db.commit()
    return {"success": True}

@router.get("/users")
def list_users(db: Session = Depends(get_db)):
    import models
    users = db.query(models.User).all()
    return [{"id": u.id, "nickname": u.nickname, "hwid": u.hwid, "active": u.active, "expire_date": u.expire_date} for u in users]

@router.post("/users/{user_id}/license")
def update_user_license(user_id: int, data: dict = Body(...), db: Session = Depends(get_db)):
    import models
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    
    days = data.get("days")
    import datetime
    if days is None:
        user.expire_date = "LIFETIME"
    else:
        user.expire_date = (datetime.date.today() + datetime.timedelta(days=int(days))).strftime("%Y-%m-%d")
    db.commit()
    return {"success": True, "expire_date": user.expire_date}

@router.post("/users/{user_id}/programs")
def update_user_programs(user_id: int, program_states: dict = Body(...), db: Session = Depends(get_db)):
    import models
    db.query(models.UserProgram).filter(models.UserProgram.user_id == user_id).delete()
    for p_id, is_active in program_states.items():
        if is_active:
            up = models.UserProgram(user_id=user_id, program_id=int(p_id), active=1)
            db.add(up)
    db.commit()
    return {"success": True}

@router.post("/users/{user_id}/toggle-block")
def toggle_block(user_id: int, db: Session = Depends(get_db)):
    import models
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")
    user.active = not user.active
    db.commit()
    return {"success": True, "active": user.active}

@router.get("/programs")
def get_all_programs(db: Session = Depends(get_db)):
    import models
    progs = db.query(models.Program).all()
    if not progs:
        # Тимчасовий фолбек, якщо таблиця порожня
        return [{"id": 1, "name": "Clicker"}, {"id": 3, "name": "OCR Scanner"}, {"id": 4, "name": "GTA Tool"}]
    return [{"id": p.id, "name": p.name} for p in progs]

@router.get("/user-programs/{user_id}")
def get_user_programs(user_id: int, db: Session = Depends(get_db)):
    import models
    rows = db.query(models.UserProgram).filter(models.UserProgram.user_id == user_id, models.UserProgram.active == 1).all()
    return {int(r.program_id): 1 for r in rows}