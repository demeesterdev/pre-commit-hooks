from __future__ import annotations

import pytest

from pre_commit_hooks_demeesterdev.check_kubernetes_secrets_are_sops_encrypted import main  # noqa: E501
from testing.util import get_resource_path


@pytest.mark.parametrize(
    ('filename', 'expected_retval'), (
        ('ok_yaml.yaml', 0),
        ('namespace_k8s.yaml', 0),
        ('bad_yaml.notyaml', 1),
        ('unencrypted_stringdata_secret_k8s.yaml', 1),
        ('unencrypted_data_secret_k8s.yaml', 1),
        ('encrypted_stringdata_secret_k8s.yaml', 0),
        ('encrypted_data_secret_k8s.yaml', 0),
        ('broken_encryption_secret_k8s.yaml', 1),
    ),
)
def test_main(filename, expected_retval):
    ret = main([get_resource_path(filename)])
    assert ret == expected_retval
