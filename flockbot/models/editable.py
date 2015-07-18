from sqlalchemy import Column, Integer, String
from flockbot.models import Base

class Editable(Base):
    __tablename__ = 'editable'

    id = Column(String, primary_key=True)
