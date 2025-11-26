import json
import logging
from pathlib import Path

from .agents.requirement_agent import RequirementAgent
from .agents.architect_agent import ArchitectAgent
from .agents.coder_agent import CoderAgent
from .agents.tester_agent import TesterAgent
from .agents.devops_agent import DevOpsAgent
from .agents.monitor_agent import MonitorAgent

# Define the output directory
OUTPUT_DIR = Path("src/outputs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

AGENTS = [
    RequirementAgent(),
    ArchitectAgent(),
    CoderAgent(),
    TesterAgent(),
    DevOpsAgent(),
    MonitorAgent(),
]

def run_pipeline(project_description: str = None):
    """
    Runs the full SDLC AI pipeline.
    """
    logger = logging.getLogger(__name__)

    context = {"project_description": project_description or "Create a minimal SDLC AI pipeline"}
    results = {}

    for agent in AGENTS:
        try:
            logger.info(f"--- Running agent: {agent.name} ---")

            # Run the agent
            out = agent.run(context)

            # Update context and results
            context.update(out)
            results[agent.name] = out

            # Persist each agent's output
            _save_output(agent.name, out)

            logger.info(f"--- Finished agent: {agent.name} ---")

        except Exception as e:
            logger.error(f"Agent {agent.name} failed: {e}", exc_info=True)
            # Decide if you want to stop the pipeline on failure
            # For now, we'll log the error and continue
            continue

    # Save the final consolidated results
    final_results_path = OUTPUT_DIR / "pipeline_results.json"
    with open(final_results_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Final pipeline results saved to {final_results_path}")

    return results

def _save_output(agent_name: str, output: dict):
    """
    Saves the output of an agent to the appropriate file.
    """
    logger = logging.getLogger(__name__)

    # The output dictionary is expected to have a single key, e.g., {"requirements": ...}
    output_key = next(iter(output))
    output_content = output[output_key]

    if agent_name == "requirement":
        filepath = OUTPUT_DIR / "requirements.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_content, f, indent=2)
    elif agent_name == "architect":
        filepath = OUTPUT_DIR / "architecture.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_content, f, indent=2)
    elif agent_name == "coder":
        filepath = OUTPUT_DIR / "main.py"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(output_content)
    elif agent_name == "tester":
        filepath = OUTPUT_DIR / "tests.py"
        unit_tests = output_content.get("unit_tests", "")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(unit_tests)
        # Also save the test cases
        test_cases_path = OUTPUT_DIR / "test_cases.json"
        with open(test_cases_path, "w", encoding="utf-8") as f:
            json.dump(output_content.get("test_cases", []), f, indent=2)
    elif agent_name == "devops":
        dockerfile_path = OUTPUT_DIR / "Dockerfile"
        with open(dockerfile_path, "w", encoding="utf-8") as f:
            f.write(output_content.get("dockerfile", ""))
        cicd_path = OUTPUT_DIR / "cicd.yml"
        with open(cicd_path, "w", encoding="utf-8") as f:
            f.write(output_content.get("cicd_pipeline", ""))
    elif agent_name == "monitor":
        filepath = OUTPUT_DIR / "monitoring.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_content, f, indent=2)
    else:
        # Fallback for any other agent
        filepath = OUTPUT_DIR / f"{agent_name}_output.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output_content, f, indent=2)

    logger.info(f"Saved output for agent '{agent_name}' to {filepath}")