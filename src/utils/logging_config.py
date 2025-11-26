import logging
import sys
from pathlib import Path

def setup_logging():
    """Set up the logger for the application."""
    log_dir = Path("src/outputs/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "pipeline.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_file, mode='w')
        ]
    )

    # Suppress noisy loggers if necessary
    logging.getLogger("httpx").setLevel(logging.WARNING)

    return logging.getLogger(__name__)