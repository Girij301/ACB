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
        workspace_snapshot: list,
    ) -> DebugSuggestion:
        """
        Analyze a failed execution and return
        an AI-generated debugging suggestion.
        """
        prompt = DEBUG_PROMPT.format(
            failure=json.dumps(failure, indent=2),
            history=json.dumps(history, indent=2),
            workspace_snapshot=json.dumps(workspace_snapshot, indent=2),
        )

        logger.info("Sending failure to Gemini Debug Agent...")

        response = self.gemini.generate_response(prompt)
        logger.info("Raw Gemini response:\n%s", response)

        logger.info("Raw Debug Response:")
        logger.info(response)

        suggestion = ResponseParser.parse_debug_response(response)

        logger.info(
            "Parsed Debug Suggestion | Files=%d Commands=%d Dependencies=%d",
            len(suggestion.files),
            len(suggestion.commands),
            len(suggestion.dependencies),
        )
        logger.info(
            "Parsed Debug Suggestion | "
            f"Files={len(suggestion.files)} "
            f"Commands={len(suggestion.commands)}"
        )

        return suggestion
