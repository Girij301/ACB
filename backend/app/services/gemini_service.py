from google import genai
from app.core.config import settings


class GeminiService:
    def __init__(self):
        # Create client using centralized config
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)

    def generate_response(self, prompt: str, model: str | None = None) -> str:
        """
        Generate response from Gemini model
        """

        model_name = model or settings.MODEL_NAME

        response = self.client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        return response.text