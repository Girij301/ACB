from sqlalchemy.orm import Session

from app.models.retry_record import RetryRecord


class RetryRepository:
    """
    Repository responsible for CRUD operations
    on RetryRecord records.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        retry: RetryRecord,
    ) -> RetryRecord:
        self.db.add(retry)
        self.db.commit()
        self.db.refresh(retry)
        return retry

    def get_by_id(
        self,
        retry_id: int,
    ) -> RetryRecord | None:
        return self.db.query(RetryRecord).filter(RetryRecord.id == retry_id).first()

    def list_by_execution(
        self,
        execution_id: int,
    ) -> list[RetryRecord]:
        return (
            self.db.query(RetryRecord)
            .filter(
                RetryRecord.execution_id == execution_id,
            )
            .order_by(
                RetryRecord.created_at.asc(),
            )
            .all()
        )

    def update(
        self,
        retry: RetryRecord,
    ) -> RetryRecord:
        self.db.commit()
        self.db.refresh(retry)
        return retry

    def delete(
        self,
        retry: RetryRecord,
    ) -> None:
        self.db.delete(retry)
        self.db.commit()
