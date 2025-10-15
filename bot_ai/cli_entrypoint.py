# bot_ai/cli_entrypoint.py
import argparse, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    raise SystemExit(0)

def main(argv=None):
    raise SystemExit(0)

if __name__ == "__main__":
    main()
