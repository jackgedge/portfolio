#!/usr/bin/env python3

import shutil
import subprocess
from pathlib import Path

wsgidav = shutil.which("wsgidav")

if wsgidav is None:
    raise RuntimeError(
        "wsgidav was not found. Activate the portfolio Conda environment first."
    )

config_file = Path(__file__).with_name("webdav-test.yaml")

subprocess.run(
    [
        wsgidav,
        "--config",
        str(config_file),
    ],
    check=True,
)
