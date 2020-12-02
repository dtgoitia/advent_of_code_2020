from pathlib import Path

from puzzles.filesystem import get_stacktrace_frame_path


def test_get_stacktrace_frame_path():
    raw_frame = '  File "/foo/bar/baz.py", line 123, in main_foo\n    kk = blah()\n'
    path = get_stacktrace_frame_path(raw_frame=raw_frame)
    assert path == Path("/foo/bar/baz.py")
