import datetime
import timeit
from pathlib import Path

from .logic import resolve

FormattedTime = str

MAX_MEASUREMENT_TIME = 60  # seconds


def get_dump_path() -> Path:
    now = datetime.datetime.now()
    timestamp = (now - datetime.timedelta(microseconds=now.microsecond)).isoformat()
    dump_path = Path(__file__).parent / f"time_measurement_{timestamp}.txt"

    return dump_path


def get_iteration_amount() -> int:
    single_iteration = timeit.timeit(resolve, number=1)
    print(f"~{single_iteration:0.5f}s per iteration")
    complete_iterations = int(MAX_MEASUREMENT_TIME // single_iteration)
    print(f"{complete_iterations} iterations")
    return complete_iterations


def measure() -> FormattedTime:
    iterations = get_iteration_amount()
    time = timeit.timeit(resolve, number=iterations)
    formatted_time = f"{time:0.5f}"

    dump_path = get_dump_path()
    dump_path.write_text(formatted_time)

    return formatted_time


if __name__ == "__main__":
    measurement = measure()
    print(f"Time: {measurement}s")
