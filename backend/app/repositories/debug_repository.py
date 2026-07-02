from app.models.debug_record import DebugRecord
from sqlalchemy.orm import Session


class DebugRepository:
    """
    Repository responsible for CRUD operations
    on DebugRecord records.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        debug_record: DebugRecord,
    ) -> DebugRecord:
        self.db.add(debug_record)
        self.db.commit()
        self.db.refresh(debug_record)
        return debug_record

    def get_by_id(
        self,
        debug_record_id: int,
    ) -> DebugRecord | None:
        return (
            self.db.query(DebugRecord).filter(DebugRecord.id == debug_record_id).first()
        )

    def list_by_execution(
        self,
        execution_id: int,
    ) -> list[DebugRecord]:
        return (
            self.db.query(DebugRecord)
            .filter(
                DebugRecord.execution_id == execution_id,
            )
            .order_by(DebugRecord.created_at.asc())
            .all()
        )

    def update(
        self,
        debug_record: DebugRecord,
    ) -> DebugRecord:
        self.db.commit()
        self.db.refresh(debug_record)
        return debug_record

    def delete(
        self,
        debug_record: DebugRecord,
    ) -> None:
        self.db.delete(debug_record)
        self.db.commit()
