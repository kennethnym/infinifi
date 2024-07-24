import datetime


def log_info(message: str):
    print(f"[INFO] {datetime.datetime.now()}: {message}")


def log_warn(message: str):
    print(f"[WARN] {datetime.datetime.now()}: {message}")
