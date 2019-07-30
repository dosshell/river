from typing import List
import datetime


has_error: bool = False
log_history: List[str] = []


def _current_time() -> str:
    precise_time = datetime.datetime.now(datetime.timezone.utc).astimezone()
    return precise_time.replace(microsecond=0).isoformat()


def log(msg: str) -> None:
    global log_history
    time: str = _current_time()
    msg: str = f"""{time}: {msg}"""
    log_history.append(msg)
    print(msg)


def error(msg: str) -> None:
    global log_history
    global has_error
    has_error = True
    time: str = _current_time()
    msg: str = f"""{time} ERROR: {msg}"""
    log_history.append(msg)
    print(msg)


def flush() -> List[str]:
    global log_history
    global has_error
    has_error = False
    tmp: List[str] = log_history
    log_history = []
    return tmp
