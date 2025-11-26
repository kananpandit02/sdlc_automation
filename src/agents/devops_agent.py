from src.utils.llm import chat_completion

SYSTEM= """
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


class DevOpsAgent:
    def run(self, context):
        code = context.get("code", "")
        messages = [
            {
                "role": "user",
                "content": f"Generate DevOps deployment setup for this FastAPI code:\n{code}"
            }
        ]
        out = chat_completion(SYSTEM, messages)
        return {"devops": out}
