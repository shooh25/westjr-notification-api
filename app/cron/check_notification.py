from datetime import datetime, timedelta, timezone
from app.services.notification import send_notification
from app.models.db import SessionLocal
from app.models.models import UserSetting

def main():
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST).strftime("%H:%M")
    
    db = SessionLocal()
    users = db.query(UserSetting).all()

    for user in users:
        print(user.user_id, user.time, now)
        if user.time == now:
            send_notification(user.user_id, user.line, user.direction)

    db.close()


if __name__ == "__main__":
    main()
