import os  # noqa: D100
import sys
from glob import glob

sys.path.append(".")


def refactor(string: str) -> str:  # noqa: D103
    return string.replace(os.path.sep, ".").replace(".py", "")


pytest_plugins = [
    refactor(fixture)
    for fixture in glob("tests/fixtures/**/*.py")
    if "__" not in fixture  # noqa: PLR2004
]
