from datetime import datetime
from app.services.user_settings import get_all_user_settings
from app.services.notification import send_notification
import asyncio

async def main():
    now = datetime.now().strftime("%H:%M")
    users = await get_all_user_settings()

    for user in users:
        if user.time == now:
            await send_notification(user.user_id)

if __name__ == "__main__":
    asyncio.run(main())
