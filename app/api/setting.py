from fastapi import APIRouter, Header, HTTPException, Depends
from app.models.models import UserSettingBase, UserSetting
from app.models.db import get_db
from sqlalchemy.orm import Session
from app.services.notification import schedule_notification
from app.services.auth import verify_user_token

router = APIRouter()

# 登録済みユーザーの確認
@router.get("/user/status")
def get_user_status(
    db: Session = Depends(get_db),
    authorization: str = Header(..., alias="Authorization")
):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    user_token = authorization.split(" ")[1]
    user_id = verify_user_token(user_token)
    exists = db.query(UserSetting).filter(UserSetting.user_id == user_id).first() is not None
    return {
        "userId": user_id,
        "isRegistered": exists
    }

# 通知設定を取得する
@router.get("/setting")
def get_user_setting(
    db: Session = Depends(get_db),
    authorization: str = Header(..., alias="Authorization")
) -> dict:
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")
    
    user_token = authorization.split(" ")[1]
    user_id = verify_user_token(user_token)
    
    user_data = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User setting not found")

    return {
        "userId": user_data.user_id,
        "line": user_data.line,
        "time": user_data.time
    }

# 通知設定を更新する
@router.post("/setting")
def update_user_setting(
    user_request: UserSettingBase,
    db: Session = Depends(get_db),
    authorization: str = Header(..., alias="Authorization")
) -> dict:
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")

    user_token = authorization.split(" ")[1]
    user_id = verify_user_token(user_token)

    user_data = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
    if user_data:
        user_data.line = user_request.line
        user_data.time = user_request.time
    else:
        user_data = UserSetting(user_id=user_id, line=user_request.line, time=user_request.time)
        db.add(user_data)
    db.commit()
    
    schedule_notification(user_id, user_request.line, user_request.time)
    return {"message": "User setting updated successfully", "user_id": user_id}

# 通知設定を削除する
@router.delete("/setting")
def delete_user_setting(
    db: Session = Depends(get_db),
    authorization: str = Header(..., alias="Authorization")
) -> dict:
    
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid Authorization header")

    user_token = authorization.split(" ")[1]
    user_id = verify_user_token(user_token)

    user_data = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User setting not found")
    
    db.delete(user_data)
    db.commit()
    return {"message": "User setting deleted successfully", "user_id": user_id}