from app.models.validation_record import ValidationRecord
from sqlalchemy.orm import Session


class ValidationRepository:
    """
    Repository responsible for CRUD operations
    on ValidationRecord records.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        validation: ValidationRecord,
    ) -> ValidationRecord:


        self.db.add(validation)
        self.db.commit()
        self.db.refresh(validation)


        return validation

    def get_by_id(
        self,
        validation_id: int,
    ) -> ValidationRecord | None:
        return (
            self.db.query(ValidationRecord)
            .filter(ValidationRecord.id == validation_id)
            .first()
        )

    def list_by_execution(
        self,
        execution_id: int,
    ) -> list[ValidationRecord]:
        return (
            self.db.query(ValidationRecord)
            .filter(
                ValidationRecord.execution_id == execution_id,
            )
            .order_by(ValidationRecord.created_at.asc())
            .all()
        )

    def update(
        self,
        validation: ValidationRecord,
    ) -> ValidationRecord:
        self.db.commit()
        self.db.refresh(validation)
        return validation

    def delete(
        self,
        validation: ValidationRecord,
    ) -> None:
        self.db.delete(validation)
        self.db.commit()
