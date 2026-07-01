import json

from app.core.logger import logger
from app.debugger.response_parser import ResponseParser
from app.prompts.debug_prompt import DEBUG_PROMPT
from app.schemas.debug import DebugSuggestion
from app.services.gemini_service import GeminiService


class DebugAgent:
    """
    Uses Gemini to analyze failed execution steps
    and generate debugging suggestions.
    """

    def __init__(
        self,
        gemini_service: GeminiService | None = None,
    ) -> None:
        self.gemini = gemini_service or GeminiService()

    def analyze(
        self,
        failure: dict,
        history: list,
    ) -> DebugSuggestion:
        """
        Analyze a failed execution and return
        an AI-generated debugging suggestion.
        """
        prompt = DEBUG_PROMPT.format(
            failure=json.dumps(failure, indent=2),
            history=json.dumps(history, indent=2),
        )

        logger.info("Sending failure to Gemini Debug Agent...")

        response = self.gemini.generate_response(prompt)

        logger.info("Received debugging suggestion from Gemini.")

        return ResponseParser.parse_debug_response(response)
