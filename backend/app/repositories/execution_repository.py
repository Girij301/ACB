from sqlalchemy.orm import Session

from app.models.execution import Execution


class ExecutionRepository:
    """
    Repository responsible for CRUD operations
    on Execution records.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, execution: Execution) -> Execution:
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        return execution

    def get_by_id(self, execution_id: int) -> Execution | None:
        return self.db.query(Execution).filter(Execution.id == execution_id).first()

    def list(self) -> list[Execution]:
        return self.db.query(Execution).order_by(Execution.created_at.desc()).all()

    def update(self, execution: Execution) -> Execution:
        self.db.commit()
        self.db.refresh(execution)
        return execution

    def delete(self, execution: Execution) -> None:
        self.db.delete(execution)
        self.db.commit()
