from app.services.gemini_service import GeminiService


class CodeGenerationService:
    def __init__(self):
        self.gemini = GeminiService()

    def generate(
        self,
        goal: str,
        relative_path: str,
    ) -> str:

        prompt = f"""
You are an expert software engineer.

Generate ONLY the complete contents of:

{relative_path}

Goal:

{goal}

Rules:
- Return only the source code.
- No markdown.
- No explanations.
- No ``` blocks.
- Generate the complete file.
"""

        return self.gemini.generate_response(prompt).strip()