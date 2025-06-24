"""
main.py - Civic Interconnect Bill Monitor Agent

Monitors OpenStates bill activity by jurisdiction daily.
"""

import os
import sys
from pathlib import Path

from civic_lib_core import config_utils, log_utils
from civic_lib_core.date_utils import today_utc_str
from civic_lib_core.path_utils import ensure_dir
from civic_lib_core.yaml_utils import write_yaml
from dotenv import load_dotenv

from agents_monitor_bills.parsers import openstates_bill_parser


def main():
    """
    Main function to run the agent.
    Expected config.yaml keys:
    - report_path
    - openstates_graphql_url
    """
    log_utils.init_logger()
    logger = log_utils.logger

    logger.info("===== Starting Monitor Bills Agent =====")
    load_dotenv()

    root_dir = Path.cwd()
    config = config_utils.load_yaml_config("config.yaml", root_dir=root_dir)
    version = config_utils.load_version("VERSION", root_dir=root_dir)
    api_key: str | None = os.getenv("OPENSTATES_API_KEY")
    today = today_utc_str()
    logger.info(f"Polling date: {today}")

    report_path = ensure_dir(Path(config["report_path"]) / today)
    logger.info(f"Report path: {report_path}")

    try:
        summary = openstates_bill_parser.run(report_path, config, api_key)
    except Exception as e:
        logger.error(f"Failed OpenStates query: {e}")
        summary = []

    report = {
        "date": today,
        "version": version,
        "total_jurisdictions": len(summary),
        "jurisdictions": summary,
    }

    report_file = report_path / f"{today}-bills-report.yaml"
    write_yaml(report, report_file)
    logger.info(f"Report created: {report_file}")


if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception:
        sys.exit(1)
