import time

import httpx
from google import genai
from google.genai.errors import ClientError, ServerError
from google.genai.types import GenerateContentConfig

from app.core.config import settings
from app.core.logger import logger


class GeminiQuotaError(Exception):
    """
    Raised when the Gemini API quota or rate limit is exceeded.
    """

    def __init__(self, message: str):
        super().__init__(message)


class GeminiService:
    """
    Wrapper around the Gemini API.

    Provides automatic retries for temporary
    server-side failures.

    Quota errors are not retried automatically.
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

    def generate_response(
        self,
        prompt: str,
        *,
        temperature: float = 0.1,
        max_output_tokens: int = 4096,
    ) -> str:
        """
        Generate a response from Gemini.

        Automatically retries temporary server failures
        using exponential backoff.

        Quota errors are raised immediately because
        retrying them only wastes time and quota attempts.
        """

        max_retries = 5

        for attempt in range(max_retries):
            try:
                response = self.client.models.generate_content(
                    model=settings.MODEL_NAME,
                    contents=prompt,
                    config=GenerateContentConfig(
                        temperature=temperature,
                        max_output_tokens=max_output_tokens,
                    ),
                )

                return response.text.strip()

            except ClientError as exc:

                # 429 = RESOURCE_EXHAUSTED
                if exc.code == 429:

                    logger.error(
                        "Gemini API quota exceeded. "
                        "Skipping automatic retry."
                    )

                    raise GeminiQuotaError(
                        "Gemini API quota exceeded. "
                        "Please try again later."
                    ) from exc

                logger.error(
                    f"Gemini client error: {exc}"
                )

                raise

            except ServerError as exc:
                retry_number = attempt + 1

                logger.warning(
                    f"Gemini temporary server error "
                    f"(attempt {retry_number}/{max_retries}): {exc}"
                )

                if retry_number == max_retries:
                    logger.error(
                        "Maximum Gemini retry attempts reached."
                    )
                    raise

                wait_time = 2**attempt

                logger.info(
                    f"Retrying Gemini request in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)

            except (
                httpx.RemoteProtocolError,
                httpx.ConnectError,
                httpx.ReadTimeout,
                httpx.ConnectTimeout,
            ) as exc:
                retry_number = attempt + 1

                logger.warning(
                    f"Gemini network error "
                    f"(attempt {retry_number}/{max_retries}): {exc}"
                )

                if retry_number == max_retries:
                    logger.error(
                        "Maximum Gemini network retry attempts reached."
                    )
                    raise

                wait_time = 2**attempt

                logger.info(
                    f"Retrying Gemini request in "
                    f"{wait_time} seconds..."
                )

                time.sleep(wait_time)