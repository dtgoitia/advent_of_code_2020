import traceback
from pathlib import Path
from typing import List


def get_stacktrace_frame_path(raw_frame: str) -> Path:
    path_as_str = raw_frame.split("File ")[1].split(", line")[0].strip('"')
    return Path(path_as_str)


def get_file_name_from_calling_function() -> Path:
    uppermost_frame_data = traceback.format_stack()[-3]
    path = get_stacktrace_frame_path(uppermost_frame_data)
    return path.parent


def get_input_paths() -> List[Path]:
    parent_path = get_file_name_from_calling_function()

    paths = sorted(parent_path.glob("input*"))

    return paths
