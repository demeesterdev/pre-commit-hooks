from __future__ import annotations

import argparse
from typing import Any
from typing import Sequence

from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError

yaml = YAML(typ='safe')


def check_doc(doc: Any) -> bool:
    if 'kind' in doc:
        if doc['kind'] == 'Secret':
            return True
    return False


def check_file(filename: str) -> tuple[bool, str]:
    with open(filename, encoding='UTF-8') as f:
        try:
            docs = list(yaml.load_all(f))
        except (ParserError, ScannerError):
            return False, f"{filename}: Not valid YAML."

        except Exception as err:  # pragma: no cover
            # All kubernetes secret are stored in yaml
            return False, f"{filename}: Unexpected {err=}, {type(err)=}"

    secrets_in_file = 0
    for doc in docs:
        contains_secret = check_doc(doc)
        if contains_secret:
            secrets_in_file += 1

    if secrets_in_file != 0:
        return False, f"{filename}: {secrets_in_file} secrets"

    return True, f"{filename}: no secrets"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*', help='Filenames to check.')
    args = parser.parse_args(argv)

    failed_messages = []
    for filename in args.filenames:
        try:
            is_valid, message = check_file(filename)
            if not is_valid:
                failed_messages.append(message)
        except Exception as exc:  # pragma: no cover
            failed_messages.append(f"{filename}: {exc}")

    if failed_messages:
        print('\n'.join(failed_messages))
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
