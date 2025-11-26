import argparse
import logging
from src.orchestrator import run_pipeline
from src.utils.logging_config import setup_logging


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    parser.add_argument("--desc", default=None, help="Short project description")
    args = parser.parse_args()

    logger.info("Starting the SDLC-AI pipeline...")
    results = run_pipeline(args.desc)
    logger.info("Pipeline finished. Outputs saved in src/outputs/")

if __name__ == '__main__':
    main()