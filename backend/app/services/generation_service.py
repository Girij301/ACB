from app.services.gemini_service import GeminiService


class CodeGenerationService:
    """
    Generates the complete contents of a single file
    during autonomous execution.
    """

    def __init__(self):
        self.gemini = GeminiService()

    def generate(
        self,
        goal: str,
        step_description: str,
        relative_path: str,
    ) -> str:
        """
        Generate the complete contents of a single file.

        Args:
            goal:
                Overall project goal.

            step_description:
                Description of the current planner step.

            relative_path:
                File to generate.
        """

        prompt = f"""
You are an autonomous senior software engineer.

You are executing ONE step of an autonomous software development pipeline.

Overall Project Goal:

{goal}

Current Execution Step:

{step_description}

Target File:

{relative_path}

Your responsibility is to generate ONLY the contents of the target file.

Important Rules:

- Generate only the requested file.
- Do NOT generate any other files.
- Do NOT explain your work.
- Do NOT describe your reasoning.
- Do NOT write tutorials.
- Do NOT include markdown.
- Do NOT include triple backticks.
- Do NOT include comments outside the source code.
- Return the COMPLETE file.
- The output will be written directly to disk.
- Keep the implementation concise and production-ready.
- If the target file is README.md, generate only a short project README suitable for the current execution step instead of a full documentation guide.

Return ONLY the file contents.
"""

        return self.gemini.generate_response(
            prompt,
            temperature=0.05,
            max_output_tokens=2048,
        )
