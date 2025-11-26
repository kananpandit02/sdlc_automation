import json
from .base_agent import BaseAgent

SYSTEM_PROMPT = """
ROLE:
You are the Monitor Agent.

PRIMARY OBJECTIVE:
Analyze logs, detect issues, and recommend optimizations.

RESPONSIBILITIES:
- Detect anomalies
- Analyze root causes
- Suggest solutions

OUTPUT FORMAT:
STRICT VALID JSON ONLY:
{
  "issue": "",
  "cause": "",
  "recommendation": ""
}

FEW-SHOT EXAMPLES:

INPUT: "Timeout errors increasing"
OUTPUT:
{
  "issue": "API Timeout",
  "cause": "Slow database queries",
  "recommendation": "Implement caching and optimize DB indexes"
}
"""


class MonitorAgent(BaseAgent):
    def __init__(self, model_name: str = "llama3"):
        super().__init__("monitor", SYSTEM_PROMPT, model_name)

    def run(self, context: dict) -> dict:
        self.logger.info("Running Monitor Agent...")
        architecture = context.get("architecture", {})

        architecture_str = json.dumps(architecture, indent=2)

        messages = [
            {
                "role": "user",
                "content": f"Based on the architecture below, generate generalized monitoring documentation:\n\n{architecture_str}"
            }
        ]

        raw_output = self._chat_completion(messages)
        parsed_output = self._parse_json(raw_output)

        self.logger.info("Monitor Agent finished.")
        return {"monitor": parsed_output}
