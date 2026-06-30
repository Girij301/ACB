import json

from app.core.logger import logger
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.schemas.planner import PlannerResponse
from app.services.gemini_service import GeminiService
from fastapi import HTTPException


class PlannerService:
    def __init__(self):
        self.gemini = GeminiService()

    def create_plan(self, task: str) -> PlannerResponse:
        """
        Generate a structured execution plan for a task.
        """

        try:
            # Build prompt
            prompt = PLANNER_PROMPT.replace("{task}", task)

            logger.info(f"Generating execution plan for task: {task}")

            # Get response from Gemini
            response = self.gemini.generate_response(prompt)

            # Remove Markdown if Gemini returns ```json ... ```
            response = response.strip()

            if response.startswith("```"):
                response = response.replace("```json", "").replace("```", "").strip()

            # Convert JSON string to Python dictionary
            plan = json.loads(response)

            logger.info("Execution plan generated successfully.")

            # Validate using Pydantic schema
            return PlannerResponse(**plan)

        except json.JSONDecodeError as e:
            logger.error(f"Gemini returned invalid JSON: {e}")

            raise HTTPException(
                status_code=500,
                detail="Planner returned an invalid JSON response.",
            )

        except Exception as e:
            logger.exception(f"Planner Service Error: {e}")

            raise HTTPException(
                status_code=500,
                detail="Failed to generate execution plan.",
            )
