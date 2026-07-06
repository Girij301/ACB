import time

from app.core.config import settings
from app.core.logger import logger
from google import genai
from google.genai.errors import ServerError
from google.genai.types import GenerateContentConfig

class GeminiService:
    """
    Wrapper around the Gemini API.

    Provides automatic retries for temporary
    server-side failures.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def generate_response(self, prompt: str) -> str:
        """
        Generate a response from Gemini.

        Automatically retries temporary
        server failures using exponential backoff.
        """

        max_retries = 5

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=settings.MODEL_NAME,
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=0.1,
                        max_output_tokens=4096,
                    ),
                )
                return response.text
            except ServerError as exc:
                retry_number = attempt + 1

                logger.warning(
                    f"Gemini temporary server error "
                    f"(attempt {retry_number}/{max_retries}): {exc}"
                )

                if retry_number == max_retries:
                    logger.error("Maximum Gemini retry attempts reached.")
                    raise

                wait_time = 2**attempt

                logger.info(f"Retrying Gemini request in {wait_time} seconds...")

                time.sleep(wait_time)
