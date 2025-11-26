from pathlib import Path
from .agents.requirement_agent import RequirementAgent
from .agents.architect_agent import ArchitectAgent
from .agents.coder_agent import CoderAgent
from .agents.tester_agent import TesterAgent
from .agents.devops_agent import DevOpsAgent
from .agents.monitor_agent import MonitorAgent
from .utils.files import save_text, save_json

AGENTS = [
    ("requirement", RequirementAgent()),
    ("architect", ArchitectAgent()),
    ("coder", CoderAgent()),
    ("tester", TesterAgent()),
    ("devops", DevOpsAgent()),
    ("monitor", MonitorAgent()),
]


def run_pipeline(project_description: str = None):
    context = {"project_description": project_description or "Create a minimal SDLC AI pipeline"}
    results = {}

    for name, agent in AGENTS:
        print(f"Running agent: {name}")
        out = agent.run(context)
        # update context and results
        context.update(out)
        results[name] = out
        # persist each agent's output
        save_text(f"{name}.txt", str(out))

    save_json("pipeline_results.json", results)
    return results