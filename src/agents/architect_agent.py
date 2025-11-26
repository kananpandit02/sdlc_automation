from src.utils.llm import chat_completion

SYSTEM= """
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


class ArchitectAgent:
    def run(self, context):
        req = context.get("requirements", "")
        messages = [
            {
                "role": "user",
                "content": f"Here are the requirements:\n{req}\n\nGenerate a realistic architecture."
            }
        ]
        out = chat_completion(SYSTEM, messages)
        return {"architecture": out}
