from __future__ import annotations

from setuptools.config.setupcfg import read_configuration

from pre_commit_hooks_demeesterdev.check_yaml import yaml


def test_entrypoint_valid_all_hooks():
    with open('.pre-commit-hooks.yaml', encoding='UTF-8') as f:
        hooks = yaml.load(f)
    config = read_configuration('setup.cfg')

    assert 'options' in config
    assert 'entry_points' in config['options']
    assert 'console_scripts' in config['options']['entry_points']

    console_scripts = config['options']['entry_points']['console_scripts']
    console_script_entries = [
        item.split('=')[0].strip() for item in console_scripts
    ]

    for hook in hooks:
        assert hook['entry'] in console_script_entries
