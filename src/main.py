import argparse
from src.orchestrator import run_pipeline


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--desc", default=None, help="Short project description")
    args = parser.parse_args()

    results = run_pipeline(args.desc)
    print("Pipeline finished. Outputs saved in src/outputs/")

if __name__ == '__main__':
    main()