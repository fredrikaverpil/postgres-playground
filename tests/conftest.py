import os
import sys
from glob import glob

sys.path.append(".")


def refactor(string: str) -> str:
    return string.replace(os.path.sep, ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture)
    for fixture in glob("tests/fixtures/**/*.py")  # noqa: PTH207
    if "__" not in fixture
]
