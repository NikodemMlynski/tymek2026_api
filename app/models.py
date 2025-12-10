from app.database import Base 
from sqlalchemy import Column, Integer, String, Boolean

class Supporter(Base):
    __tablename__ = "Supporter"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    class_ = Column(String, nullable=False)
    approved = Column(Boolean, nullable=False)