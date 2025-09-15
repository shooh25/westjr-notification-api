from fastapi import HTTPException
import httpx
import os
from app.const import LINE_PROFILE_URL

# access_tokenを検証し、user_idを取得する
def verify_access_token(access_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    res = httpx.get(LINE_PROFILE_URL, headers=headers)

    if res.status_code != 200:
        raise HTTPException(status_code=401, detail=f"Failed to fetch user info: {res.text}")

    data = res.json()
    return data

