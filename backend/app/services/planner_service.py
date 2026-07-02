import json

from fastapi import HTTPException
from google.genai.errors import APIError

from app.core.logger import logger
from app.prompts.planner_prompt import PLANNER_PROMPT
from app.schemas.planner import PlannerResponse
from app.services.gemini_service import GeminiService


class PlannerService:
    def __init__(self):
        self.gemini = GeminiService()

    def create_plan(self, task: str) -> PlannerResponse:
        """
        Generate a structured execution plan for a task.
        """

        prompt = PLANNER_PROMPT.replace("{task}", task)

        logger.info(f"Generating execution plan for task: {task}")

        try:
            response = self.gemini.generate_response(prompt)

            response = response.strip()

            if response.startswith("```"):
                response = (
                    response.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            logger.info("Raw Gemini response:")
            logger.info(response)

            plan = json.loads(response)

            return PlannerResponse(**plan)

        except json.JSONDecodeError as e:
            logger.exception("Gemini returned invalid JSON")

            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Planner returned invalid JSON.",
                    "raw_response": response if "response" in locals() else None,
                    "error": str(e),
                },
            )

        except APIError as e:
            logger.exception("Gemini API Error")

            raise HTTPException(
                status_code=503,
                detail={
                    "message": "Gemini API unavailable.",
                    "error": str(e),
                },
            )

        except Exception as e:
            logger.exception("Planner Service Error")

            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Planner Service Error",
                    "error": str(e),
                },
            )