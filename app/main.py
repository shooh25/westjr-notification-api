from fastapi import FastAPI, Request, Header, HTTPException, Depends
import httpx
import os
from dotenv import load_dotenv
from app.westjr_client import get_attention_messages
from app.db import SessionLocal
from app.models import UserSettingBase, UserSetting
from sqlalchemy.orm import Session

load_dotenv()
app = FastAPI()

# メッセージをLINEに返信するための設定
LINE_API_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
LINE_VERIFY_URL = "https://api.line.me/oauth2/v2.1/verify"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')}"
}

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# user_tokenを検証し、user_idを取得する
def verify_user_token(user_token: str) -> str:
    params = {
        "user_token": user_token,
        "client_id": os.getenv("LINE_CLIENT_ID")
    }
    res = httpx.post(LINE_VERIFY_URL, params=params)
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid ID token")

    data = res.json()
    user_id = data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return user_id

# 登録済みユーザーの確認
@app.get("/user/status")
def get_user_status(
    db: Session = Depends(get_db),
    user_token: str = Header(..., alias="User-Token")
):
    user_id = user_token
    exists = db.query(UserSetting).filter(UserSetting.user_id == user_id).first() is not None
    return {
        "user_id": user_id,
        "isRegistered": exists
    }

# 通知設定を取得する
@app.get("/setting")
def get_user_setting(
    db: Session = Depends(get_db),
    user_token: str = Header(..., alias="User-Token")
):
    user_id = user_token  

    user_data = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
    if not user_data:
        raise HTTPException(status_code=404, detail="User setting not found")

    return {
        "user_id": user_data.user_id,
        "line": user_data.line,
        "time": user_data.time
    }

        
# 通知設定を更新する
@app.post("/setting")
def update_user_setting(
    user_request: UserSettingBase,
    db: Session = Depends(get_db),
    user_token: str = Header(..., alias="User-Token"),
):

    # user_id = verify_user_token(user_token)
    user_id = user_token
    user_data = db.query(UserSetting).filter(UserSetting.user_id == user_id).first()
    if user_data:
        print("exist user")
        user_data.line = user_request.line
        user_data.time = user_request.time
    else:
        print("new user")
        user_data = UserSetting(user_id=user_id, line=user_request.line, time=user_request.time)
        db.add(user_data)
    db.commit()
    return {"message": "User setting updated successfully", "user_id": user_id}
    

# Lineからメッセージを受信する際のエンドポイント
# reply_token : 即座に返信するために必要なトークン
@app.post("/notification")
async def line_webhook(request: Request):
    body = await request.json()
    events = body.get("events", [])
    print(body)
    for event in events:
        if event["type"] == "message":
            reply_token = event["replyToken"]
            user_message = event["message"]["text"].strip()
            words = user_message.split()
            if len(words) == 2:
                attention_messages = get_attention_messages(words[0], int(words[1]))
                response_text = "\n".join(attention_messages)
            else:
                response_text = "正しくありません"
            
            payload = {
                "replyToken": reply_token,
                "messages": [
                    {
                        "type": "text",
                        "text": response_text
                    }
                ]
            }

            async with httpx.AsyncClient() as client:
                await client.post(LINE_API_REPLY_URL, headers=HEADERS, json=payload)
