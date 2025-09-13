from fastapi import HTTPException
import httpx
import os
from app.const import LINE_VERIFY_URL

# user_tokenを検証し、user_idを取得する
def verify_user_token(user_token: str) -> str:
    payload = {
        "id_token": user_token,
        "client_id": os.getenv("LINE_CLIENT_ID")
    }
    res = httpx.post(LINE_VERIFY_URL, data=payload)
    if res.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid ID token")

    data = res.json()
    user_id = data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID not found in token")
    return user_id
