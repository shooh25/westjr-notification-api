from datetime import datetime
from app.services.notification import send_notification
from app.models.db import SessionLocal
from app.models.models import UserSetting

def main():
    now = datetime.now().strftime("%H:%M")
    db = SessionLocal()
    users = db.query(UserSetting).all()

    for user in users:
        if user.time == now:
            send_notification(user.user_id, user.line, user.direction)

    db.close()


if __name__ == "__main__":
    main()
