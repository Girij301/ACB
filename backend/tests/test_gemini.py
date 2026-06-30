from app.services.gemini_service import GeminiService


def test_gemini_service_init():
    service = GeminiService()
    assert service is not None
