from fastapi import FastAPI, Request
import httpx
import os
from dotenv import load_dotenv
from app.westjr_client import get_attention_messages

load_dotenv()
app = FastAPI()

# メッセージをLINEに返信するための設定
LINE_API_REPLY_URL = "https://api.line.me/v2/bot/message/reply"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')}"
}

# Lineからメッセージを受信する際のエンドポイント
# reply_token : 即座に返信するために必要なトークン
@app.post("/")
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
