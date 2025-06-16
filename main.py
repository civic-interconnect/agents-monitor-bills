"""
main.py - Civic Interconnect Bill Monitor Agent

Monitors OpenStates bill activity by jurisdiction daily.
"""

import os
import yaml
from datetime import datetime, timezone
from dotenv import load_dotenv
from parsers import openstates_bill_parser
from loguru import logger

# Initialize logger
os.makedirs("logs", exist_ok=True)
logger.add("logs/{time:YYYY-MM-DD}.log", rotation="1 day", retention="7 days", level="INFO")

logger.info("===== Starting Bill Monitor Agent =====")

# Load environment variables
load_dotenv()

# Load API key
openstates_api_key = os.getenv("OPENSTATES_API_KEY")
if not openstates_api_key:
    logger.error("OpenStates API key missing in environment!")
    exit(1)

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

# Load version
with open("VERSION") as f:
    version = f.read().strip()
logger.info(f"Agent version: {version}")

# Today's timestamp
today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

# Create storage paths
os.makedirs("reports", exist_ok=True)
report_path = os.path.join("reports", f"{today}-bill-monitor.yaml")

# Query OpenStates
try:
    summary = openstates_bill_parser.run(".", config, openstates_api_key)
except Exception as e:
    logger.error(f"Failed OpenStates query: {e}")
    summary = []

# Build daily report
report = {
    "date": today,
    "total_jurisdictions": len(summary),
    "jurisdictions": summary
}

# Write report
with open(report_path, "w") as f:
    yaml.dump(report, f, sort_keys=False)

logger.info(f"Report written: {report_path}")
