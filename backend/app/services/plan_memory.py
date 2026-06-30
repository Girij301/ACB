import json

from app.core.database import SessionLocal
from app.core.logger import logger
from app.models.plan import Plan


def save_plan(
    session_id: str,
    user_task: str,
    plan: dict,
):

    db = SessionLocal()

    try:

        new_plan = Plan(
            session_id=session_id,
            user_task=user_task,
            plan=json.dumps(plan),
        )

        db.add(new_plan)
        db.commit()

        logger.info("Plan saved successfully.")

    except Exception as e:

        db.rollback()

        logger.exception(f"Database Error: {str(e)}")

        raise

    finally:

        db.close()
