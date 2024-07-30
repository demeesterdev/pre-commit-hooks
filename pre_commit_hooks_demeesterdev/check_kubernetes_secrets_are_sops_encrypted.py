from __future__ import annotations

import argparse
from typing import Any
from typing import Sequence

from ruamel.yaml import YAML
from ruamel.yaml.parser import ParserError
from ruamel.yaml.scanner import ScannerError

yaml = YAML(typ='safe')


def validate_enc(item: Any) -> bool:
    """
    Validate given item is encrypted.

    All leaf values in a sops encrypted file must be strings that
    start with ENC[. We iterate through lists and dicts, checking
    only for leaf strings. Presence of any other data type (like
    bool, number, etc) also makes the file invalid except an empty
    string which would pass the encryption check.
    """

    if isinstance(item, str):  # pragma: no cover
        if item == '' or item.startswith('ENC['):
            return True

    return False


def check_doc(doc: Any) -> tuple[bool, str]:
    if 'kind' not in doc:
        return True, 'yaml definition not of k8s kind'

    if doc['kind'] != 'Secret':
        return True, 'not a k8s secret'

    # from here on out we are dealing with a secret
    if 'sops' not in doc:
        # sops puts a `sops` key in the encrypted output. If it is not
        # present, very likely the file is not encrypted.
        return False, (
            'sops metadata key not found in file'
            'is not properly encrypted'
        )

    invalid_keys = []
    if 'data' in doc:
        data = doc['data']
        for k in data:
            # Values under the `sops` key are not encrypted.
            if not validate_enc(data[k]):
                # Collect all invalid keys so we can provide
                # useful error message
                invalid_keys.append(k)

    if 'stringData' in doc:
        stringdata = doc['stringData']
        for k in stringdata:
            # Values under the `sops` key are not encrypted.
            if not validate_enc(stringdata[k]):
                # Collect all invalid keys so we can provide
                # useful error message
                invalid_keys.append(k)

    if invalid_keys:
        return False, (
            'Unencrypted values found nested under'
            f"(string)data keys: {','.join(invalid_keys)}"
        )

    return True, 'Valid encryption'


def check_file(filename: str) -> tuple[bool, str]:
    with open(filename, encoding='UTF-8') as f:
        try:
            docs = list(yaml.load_all(f))
        except (ParserError, ScannerError):
            return False, f"{filename}: Not valid YAML."

        except Exception as err:  # pragma: no cover
            # All kubernetes secret are stored in yaml
            return False, f"{filename}: Unexpected {err=}, {type(err)=}"

    failed_messages = []
    for doc in docs:
        is_ok, message = check_doc(doc)
        if not is_ok:
            failed_messages.append(message)

    if failed_messages:
        return False, f"{filename} does not pass" + ','.join(failed_messages)

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
        except Exception as err:  # pragma: no cover
            failed_messages.append(
                f"{filename}:"
                f"Unexpected {err=}, {type(err)=}",
            )

    if failed_messages:
        print('\n'.join(failed_messages))
        return 1

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
