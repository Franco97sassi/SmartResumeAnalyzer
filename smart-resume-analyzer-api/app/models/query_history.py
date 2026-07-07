from sqlalchemy import Column, Integer, Text
from app.database import Base

class QueryHistory(Base):

    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)

    question = Column(Text)

    answer = Column(Text)