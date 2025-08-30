from sqlalchemy import Column, String
from app.models.db import Base
from pydantic import BaseModel
from typing import Union, Optional, List
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

class Dest(BaseModel):
    text: str
    code: str
    line: str

class TrainsItem(BaseModel):
    no: str
    pos: str
    direction: int
    nickname: Union[Optional[str], Optional[List[str]]]
    type: str
    displayType: str
    dest: Union[Dest, str]
    via: Optional[str] = None
    delayMinutes: int
    aSeatInfo: Optional[str] = None
    typeChange: Optional[str] = None
    numberOfCars: Optional[int] = None