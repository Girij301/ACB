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

        logger.info("=" * 80)
        logger.info("Generating execution plan")
        logger.info(f"Task: {task}")
        logger.info(f"Prompt Length: {len(prompt)}")
        logger.info("=" * 80)

        try:
            # -----------------------------
            # Call Gemini
            # -----------------------------
            response = self.gemini.generate_response(prompt)

            if not response:
                raise HTTPException(
                    status_code=500,
                    detail="Gemini returned an empty response.",
                )

            logger.info("Raw Gemini Response:")
            logger.info(response)

            # -----------------------------
            # Cleanup Markdown
            # -----------------------------
            response = response.strip()

            if response.startswith("```"):
                response = (
                    response.replace("```json", "")
                    .replace("```", "")
                    .strip()
                )

            # -----------------------------
            # Extract JSON only
            # -----------------------------
            start = response.find("{")
            end = response.rfind("}")

            if start == -1 or end == -1:
                raise HTTPException(
                    status_code=500,
                    detail={
                        "message": "Planner did not return valid JSON.",
                        "raw_response": response,
                    },
                )

            response = response[start : end + 1]

            logger.info("Extracted JSON:")
            logger.info(response)

            # -----------------------------
            # Parse JSON
            # -----------------------------
            plan = json.loads(response)

            logger.info(
                f"Planner generated {len(plan.get('plan', []))} steps."
            )

            return PlannerResponse(**plan)

        except json.JSONDecodeError as e:
            logger.exception("Planner returned invalid JSON")

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

        except HTTPException:
            raise

        except Exception as e:
            logger.exception("Planner Service Error")

            raise HTTPException(
                status_code=500,
                detail={
                    "message": "Planner Service Error",
                    "error": str(e),
                },
            )