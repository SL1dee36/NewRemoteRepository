"""Logging helper module."""

import datetime


def log_action(action: str, level: str = "INFO"):
    print(f"[{datetime.datetime.now()}] [{level}] ACTION: {action}")
