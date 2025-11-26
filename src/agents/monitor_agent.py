from src.utils.llm import chat_completion

SYSTEM= """
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

class MonitorAgent:
    def run(self, context):
        architecture = context.get("architecture", "")
        messages = [
            {
                "role": "user",
                "content": f"Based on the architecture below, generate generalized monitoring documentation:\n\n{architecture}"
            }
        ]
        out = chat_completion(SYSTEM, messages)
        return {"monitor": out}
