"""
Logger setup — writes to logs/agent.log and stdout.
"""
import logging
import os
from datetime import datetime


def setup_logger(level: int = logging.INFO):
    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join("logs", "agent.log")

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )
