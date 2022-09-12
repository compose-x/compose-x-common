#!/usr/bin/env python

import argparse
import json
import re
from typing import Optional, Sequence

ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:(?P<service>[\w\-_]+)?:(?P<region>[\w\-_]+)?:(?P<accountid>[0-9]{12})?(?P<resource>.*)$"
)
PLACEHOLDER = "REDACTED"


def cleanup_lists(list_content):
    for count, item in enumerate(list_content):
        if isinstance(item, dict):
            cleanup_placebo_arns(list_content)
        elif isinstance(item, list):
            cleanup_lists(item)
        elif isinstance(item, str):
            if ARN_RE.match(item):
                list_content[count] = re.sub(
                    ARN_RE.match(item).group("accountid"), "000000000000", item
                )


def cleanup_placebo_arns(file_content):
    if isinstance(file_content, dict):
        for key, value in file_content.items():
            if key in ["AccessKeyId", "SecretAccessKey", "SessionToken"] and isinstance(
                value, str
            ):
                file_content[key] = value.replace(value[0:8], PLACEHOLDER[0:8])
            if isinstance(value, dict):
                cleanup_placebo_arns(value)
            elif isinstance(value, list):
                cleanup_lists(value)
            elif isinstance(value, str):
                if ARN_RE.match(value):
                    file_content[key] = re.sub(
                        ARN_RE.match(value).group("accountid"), "000000000000", value
                    )


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check.")
    args = parser.parse_args(argv)

    retval = 0
    for filename in args.filenames:
        try:
            with open(filename, "rb") as f:
                data = json.load(f)
            cleanup_placebo_arns(data)
            with open(filename, "w") as fd:
                json.dump(data, fd, indent=4)
                fd.write("\n")
        except ValueError as exc:
            print(f"{filename}: Failed to json decode ({exc})")
            retval = 1
    return retval


if __name__ == "__main__":
    raise SystemExit(main())
