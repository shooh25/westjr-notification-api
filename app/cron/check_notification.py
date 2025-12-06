from datetime import datetime, timedelta, timezone
import time
from app.services.notification import send_notification
from app.models.db import SessionLocal
from app.models.models import UserSetting

def main():
    JST = timezone(timedelta(hours=+9), 'JST')
    now = datetime.now(JST).strftime("%H:%M")

    start = time.time()

    with SessionLocal() as db:
        users = db.query(UserSetting).filter(UserSetting.time == now).all()

        for user in users:
            print(user.time)
            send_notification(user.user_id, user.line, user.direction)

    elapsed = time.time() - start
    print(f"[INFO] Execution finished in {elapsed:.3f} sec")


if __name__ == "__main__":
    main()
