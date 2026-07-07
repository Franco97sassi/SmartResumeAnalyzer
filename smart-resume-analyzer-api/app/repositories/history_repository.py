from app.database import SessionLocal
from app.models.query_history import QueryHistory


class HistoryRepository:

    def save(self, question: str, answer: str):

        db = SessionLocal()

        history = QueryHistory(
            question=question,
            answer=answer
        )

        db.add(history)

        db.commit()

        db.close()

    def get_all(self):

        db = SessionLocal()

        data = db.query(QueryHistory).all()

        db.close()

        return data