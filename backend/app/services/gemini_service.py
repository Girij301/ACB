from app.core.config import settings
from app.core.logger import logger
from google import genai


class GeminiService:
    def __init__(self):
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_response(self, prompt: str, model: str | None = None) -> str:
        model_name = model or settings.MODEL_NAME

        logger.info(f"Gemini Request | Model: {model_name} | Prompt: {prompt}")

        try:
            response = self.client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            result = response.text

            logger.info(f"Gemini Response: {result}")

            return result

        except Exception as e:
            logger.error(f"Gemini Error: {str(e)}")
            raise
