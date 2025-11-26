import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """
ROLE:
You are the Coder Agent — an expert senior software engineer.

PRIMARY OBJECTIVE:
Generate clean, secure, production-ready code that runs immediately without modification.

RESPONSIBILITIES:
- Write COMPLETE real code (NO placeholders, NO stubs)
- Include all necessary imports
- Follow best practices and modular structure
- Add example usage or __main__ block when needed
- Output must be runnable as-is
- Output ONLY Python code blocks

OUTPUT FORMAT (MANDATORY):
You MUST output ONLY a code block like:

```python
# runnable code here
"""


class CoderAgent(BaseAgent):
    def __init__(self, model_name: str = "codellama"):
        super().__init__("coder", SYSTEM_PROMPT, model_name)

    def run(self, context: dict) -> dict:
        self.logger.info("Running Coder Agent...")
        architecture = context.get("architecture", {})

        architecture_str = json.dumps(architecture, indent=2)

        messages = [
            {
                "role": "user",
                "content": f"Architecture:\n{architecture_str}\n\nGenerate complete Python FastAPI code."
            }
        ]

        raw_output = self._chat_completion(messages)
        code = self._extract_code(raw_output)

        self.logger.info("Coder Agent finished.")
        return {"code": code}

    def _extract_code(self, raw_output: str) -> str:
        """Extracts the Python code from the LLM's raw output."""
        if "```python" in raw_output:
            return raw_output.split("```python")[1].split("```")[0].strip()
        return raw_output
