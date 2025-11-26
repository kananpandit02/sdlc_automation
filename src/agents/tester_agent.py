from src.utils.llm import chat_completion

SYSTEM= """
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


class TesterAgent:
    def run(self, context):
        code = context.get("code", "")
        messages = [
            {
                "role": "user",
                "content": f"Here is the codebase:\n{code}\n\nGenerate realistic Python pytest-based tests for this service."
            }
        ]
        out = chat_completion(SYSTEM, messages)
        return {"tests": out}
