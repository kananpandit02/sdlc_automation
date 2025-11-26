import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """
ROLE:
You are the Architect Agent, expert in creating technical software architecture.

PRIMARY OBJECTIVE:
Convert requirements into complete system architecture.

RESPONSIBILITIES:
- Identify components
- Define API endpoints
- Define processing flow
- Design database schema

OUTPUT FORMAT:
STRICT VALID JSON ONLY:
{
  "components": [],
  "flow_steps": [],
  "api_design": [],
  "database_design": []
}

FEW-SHOT EXAMPLES:

INPUT: "Login system"
OUTPUT:
{
  "components": ["Login UI", "Auth API", "JWT Service", "Users table"],
  "flow_steps": [
    "User enters credentials",
    "API verifies credentials",
    "JWT token returned"
  ],
  "api_design": ["POST /login"],
  "database_design": ["users(id, username, password_hash)"]
}

INPUT: "CSV upload"
OUTPUT:
{
  "components": ["Upload UI", "CSV API", "Validator"],
  "flow_steps": ["Upload file", "Validate file", "Store results"],
  "api_design": ["POST /upload_csv"],
  "database_design": ["import_logs(id, file_name, status)"]
}
"""


class ArchitectAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3"):
        super().__init__("architect", SYSTEM_PROMPT, model_name)

    def run(self, context: dict) -> dict:
        self.logger.info("Running Architect Agent...")
        requirements = context.get("requirements", {})

        # Ensure requirements are in a string format for the prompt
        requirements_str = json.dumps(requirements, indent=2)

        messages = [
            {
                "role": "user",
                "content": f"Here are the requirements:\n{requirements_str}\n\nGenerate a realistic architecture."
            }
        ]

        raw_output = self._chat_completion(messages)
        parsed_output = self._parse_json(raw_output)

        self.logger.info("Architect Agent finished.")
        return {"architecture": parsed_output}
