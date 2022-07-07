from sqlalchemy import Column, BigInteger, String, sql

from utils.db_api.db_gino import TimedBaseModel


class Registration(TimedBaseModel):
    __tablename__ = 'regdata'
    user_id = Column(BigInteger, primary_key=True)
    tg_first_name = Column(String(200))
    tg_last_name = Column(String(200))
    name = Column(String(200))
    lastname = Column(String(200))
    fname = Column(String(200))
    phone = Column(String(20))
    email = Column(String(200))
    status = Column(String(25))

    query: sql.select
