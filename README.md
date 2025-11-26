# SDLC-AI (Ollama local LLM)

## Prerequisites
1. Install Ollama: https://ollama.com/download
2. Pull model: e.g. `ollama pull llama3.1:8b`
3. Start Ollama (it runs as a local service): `ollama run llama3.1:8b` (or use the Ollama daemon)

## Setup
1. Create a virtualenv and install dependencies:
   python -m venv venv
   source venv/bin/activate   # on Linux/Mac
   venv\Scripts\activate     # on Windows
   pip install -r requirements.txt

2. (Optional) Set environment variables if Ollama URL/model differs:
   export OLLAMA_URL="http://localhost:11434/api/generate"
   export OLLAMA_MODEL="llama3.1:8b"

## Run
python -m src.main --desc "Build me a python microservice that responds to health checks"

Outputs will be saved to `src/outputs/`