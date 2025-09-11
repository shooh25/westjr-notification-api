import os
import httpx
from app.services.westjr_client import get_attention_messages
from sqlalchemy.orm import Session
from app.models.db import get_db
from app.models.models import UserSetting
from apscheduler.schedulers.background import BackgroundScheduler
from app.const import LINE_API_PUSH_URL

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('LINE_CHANNEL_ACCESS_TOKEN')}"
}

scheduler = BackgroundScheduler(timezone="Asia/Tokyo")

# 遅延情報を通知する
def send_notification(user_id: str, line: str):
    messages = get_attention_messages(line, 1)
    response_text = "\n".join(messages)
    print(response_text, flush=True)    
    payload = {
        "to": user_id,
        "messages": [
            {
                "type": "text",
                "text": response_text
            }
        ]
    }

    with httpx.Client() as client:
        client.post(
            LINE_API_PUSH_URL,
            headers=headers,
            json=payload
        )

# ユーザーごとに通知スケジュールを設定する
def schedule_notification(user_id: str, line: str, time: str):
    hour, minute = map(int, time.split(":"))
    # scheduler.add_job(
	# 	func=send_notification,
	# 	trigger="cron",
	# 	hour=hour,
	# 	minute=minute,
	# 	args=[user_id, line],
	# 	id=user_id,
	# 	replace_existing=True,
	# )
    
# スケジューラーを起動する
def start_scheduler():
    db = next(get_db())
    users = db.query(UserSetting).all()
    for user in users:
        schedule_notification(user.user_id, user.line, user.time)
    scheduler.start()

