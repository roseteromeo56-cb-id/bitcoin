#!/usr/bin/env python3
#
# Copyright (c) 2026 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

"""
Check that first-party C and C++ code does not use raw readlink calls.
"""

import re
import subprocess
import sys

EXCLUDED_PATHS = [
    "src/leveldb/**",
    "src/crc32c/**",
    "src/secp256k1/**",
    "src/minisketch/**",
]


def main() -> int:
    command = [
        "git",
        "grep",
        "-n",
        "-E",
        r"\breadlink[[:space:]]*\(",
        "--",
        "*.c",
        "*.cc",
        "*.cpp",
        "*.h",
    ] + [f":!:{path}" for path in EXCLUDED_PATHS]

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            return 0
        print(e.output, end="")
        return 1

    matches = [line for line in output.splitlines() if not re.search(r"lint-raw-readlink\.py", line)]
    if matches:
        print("Raw readlink calls are not allowed in first-party C/C++ code.")
        print("Use std::filesystem::read_symlink through fs::read_symlink instead.")
        print("\n".join(matches))
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
