from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from app.db import Base
from pydantic import BaseModel

class UserSetting(Base):
    __tablename__ = "user_settings"
    user_id = Column(String, primary_key=True, index=True)
    line = Column(String)
    time = Column(String)

class UserSettingBase(BaseModel):
    line: str
    time: str
    class Config:
      orm_mode = True