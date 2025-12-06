from sqlalchemy import select
from app.models.models import UserSettingBase, UserSetting
from app.models.db import get_db

async def get_all_user_settings():
    async with get_db() as session:
        result = await session.execute(select(UserSetting))
        return result.scalars().all()
