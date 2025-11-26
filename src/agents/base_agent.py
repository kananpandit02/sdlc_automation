import json
import logging
from abc import ABC, abstractmethod
from typing import Dict, List
from ..utils.llm import chat_completion, LLMError

class BaseAgent(ABC):
    """Abstract base class for all agents."""

    def __init__(self, name: str, system_prompt: str, model_name: str = None):
        self.name = name
        self.system_prompt = system_prompt
        self.model_name = model_name
        self.logger = logging.getLogger(f"agent.{self.name}")

    def _chat_completion(self, messages: List[Dict[str, str]], max_retries: int = 1) -> str:
        """Wrapper around chat_completion with retry logic."""
        for attempt in range(max_retries + 1):
            try:
                return chat_completion(self.system_prompt, messages, self.model_name)
            except LLMError as e:
                self.logger.error(f"LLM call failed on attempt {attempt + 1}: {e}")
                if attempt >= max_retries:
                    raise
        return "" # Should be unreachable

    def _parse_json(self, json_string: str) -> Dict:
        """Parse a JSON string, with error handling."""
        try:
            # The LLM sometimes wraps the JSON in ```json ... ```, so we strip that
            if json_string.startswith("```json"):
                json_string = json_string[7:-4].strip()
            return json.loads(json_string)
        except json.JSONDecodeError:
            self.logger.error(f"Failed to parse JSON output: {json_string}")
            raise ValueError("Invalid JSON format from LLM.")

    @abstractmethod
    def run(self, context: dict) -> dict:
        """The main execution method for the agent."""
        pass
