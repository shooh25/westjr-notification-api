import httpx
import os
from fastapi import Request
from app.services.westjr_client import get_attention_messages
from app.main import app
from app.const import LINE_API_REPLY_URL

# Lineからメッセージを受信する際のエンドポイント
# reply_token : 即座に返信するために必要なトークン
# @app.post("/notification")
# async def line_webhook(request: Request):
#     body = await request.json()
#     events = body.get("events", [])
#     print(body)
#     for event in events:
#         if event["type"] == "message":
#             reply_token = event["replyToken"]
#             user_message = event["message"]["text"].strip()
#             words = user_message.split()
#             if len(words) == 2:
#                 attention_messages = get_attention_messages(words[0], int(words[1]))
#                 response_text = "\n".join(attention_messages)
#             else:
#                 response_text = "正しくありません"
            
#             payload = {
#                 "replyToken": reply_token,
#                 "messages": [
#                     {
#                         "type": "text",
#                         "text": response_text
#                     }
#                 ]
#             }

#             async with httpx.AsyncClient() as client:
#                 await client.post(LINE_API_REPLY_URL, headers=HEADERS, json=payload)
