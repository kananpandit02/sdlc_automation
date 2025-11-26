from .base_agent import BaseAgent

SYSTEM_PROMPT = """
ROLE:
You are the DevOps Agent, expert in CI/CD and infrastructure automation.

PRIMARY OBJECTIVE:
Generate deployment configuration (Dockerfile, GitHub Actions, etc.)

RESPONSIBILITIES:
- Create Dockerfile
- Create CI/CD pipeline
- Optimize deployment workflow

OUTPUT FORMAT:
STRICT VALID JSON ONLY:
{
  "dockerfile": "string",
  "cicd_pipeline": "string"
}

FEW-SHOT EXAMPLES:

INPUT: "Deploy FastAPI"
OUTPUT:
{
  "dockerfile": "FROM python:3.10\\nCOPY . .\\nRUN pip install -r requirements.txt\\nCMD ['uvicorn','app:app','--host','0.0.0.0']",
  "cicd_pipeline": "name: CI\\non: [push]\\njobs:\\n  build:\\n    runs-on: ubuntu-latest\\n    steps:\\n      - run: pip install -r requirements.txt\\n      - run: pytest"
}
"""


class DevOpsAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3"):
        super().__init__("devops", SYSTEM_PROMPT, model_name)

    def run(self, context: dict) -> dict:
        self.logger.info("Running DevOps Agent...")
        code = context.get("code", "")

        messages = [
            {
                "role": "user",
                "content": f"Generate DevOps deployment setup for this FastAPI code:\n{code}"
            }
        ]

        raw_output = self._chat_completion(messages)
        parsed_output = self._parse_json(raw_output)

        self.logger.info("DevOps Agent finished.")
        return {"devops": parsed_output}
