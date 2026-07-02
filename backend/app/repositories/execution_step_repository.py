from app.models.execution_step import ExecutionStep
from sqlalchemy.orm import Session


class ExecutionStepRepository:
    """
    Repository responsible for CRUD operations
    on ExecutionStep records.
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, step: ExecutionStep) -> ExecutionStep:
        self.db.add(step)
        self.db.commit()
        self.db.refresh(step)
        return step

    def get_by_id(self, step_id: int) -> ExecutionStep | None:
        return self.db.query(ExecutionStep).filter(ExecutionStep.id == step_id).first()

    def list_by_execution(
        self,
        execution_id: int,
    ) -> list[ExecutionStep]:
        return (
            self.db.query(ExecutionStep)
            .filter(
                ExecutionStep.execution_id == execution_id,
            )
            .order_by(ExecutionStep.step_index.asc())
            .all()
        )

    def update(
        self,
        step: ExecutionStep,
    ) -> ExecutionStep:
        self.db.commit()
        self.db.refresh(step)
        return step

    def delete(self, step: ExecutionStep) -> None:
        self.db.delete(step)
        self.db.commit()
