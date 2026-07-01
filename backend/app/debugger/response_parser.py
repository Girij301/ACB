import json

from app.schemas.debug import DebugSuggestion


class ResponseParser:
    """
    Parses Gemini responses into structured models.
    """

    @staticmethod
    def parse_debug_response(
        response: str,
    ) -> DebugSuggestion:
        """
        Parse a Gemini JSON response into a DebugSuggestion.
        """

        cleaned = response.strip()

        # Remove Markdown code fences if present
        if cleaned.startswith("```json"):
            cleaned = cleaned.removeprefix("```json").strip()

        if cleaned.startswith("```"):
            cleaned = cleaned.removeprefix("```").strip()

        if cleaned.endswith("```"):
            cleaned = cleaned.removesuffix("```").strip()

        data = json.loads(cleaned)

        return DebugSuggestion.model_validate(data)
