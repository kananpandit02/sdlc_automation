from .base_agent import BaseAgent

SYSTEM_PROMPT = """
ROLE:
You are the Tester Agent, expert in QA and automated testing.

PRIMARY OBJECTIVE:
Generate high-quality test cases and automated tests.

RESPONSIBILITIES:
- Create manual test cases
- Create unit tests
- Identify edge cases

OUTPUT FORMAT:
STRICT VALID JSON ONLY:
{
  "test_cases": [],
  "unit_tests": "string"
}

FEW-SHOT EXAMPLES:

INPUT: "Login API"
OUTPUT:
{
  "test_cases": [
    {"title": "Valid Login", "expected": "200 OK with token"},
    {"title": "Invalid Login", "expected": "401 Unauthorized"}
  ],
  "unit_tests": "def test_valid_login(client):\\n    r=client.post('/login',json={'username':'admin','password':'123'})\\n    assert r.status_code==200"
}
"""


class TesterAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3"):
        super().__init__("tester", SYSTEM_PROMPT, model_name)

    def run(self, context: dict) -> dict:
        self.logger.info("Running Tester Agent...")
        code = context.get("code", "")

        messages = [
            {
                "role": "user",
                "content": f"Here is the codebase:\n{code}\n\nGenerate realistic Python pytest-based tests for this service."
            }
        ]

        raw_output = self._chat_completion(messages)
        parsed_output = self._parse_json(raw_output)

        self.logger.info("Tester Agent finished.")
        return {"tests": parsed_output}
