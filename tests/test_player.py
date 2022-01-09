#!/usr/bin/env python3
# coding=utf-8
from configparser import ConfigParser
from pathlib import Path

import pytest

from ogsdownloader.oauth2 import get_token
from ogsdownloader.player import Player


@pytest.fixture(scope='session')
def config() -> ConfigParser:
    config = ConfigParser()
    config.read('test_config.cfg')
    if not config.has_option('DEFAULT', 'refresh_token'):
        tokens = get_token(config)
        config['DEFAULT']['refresh_token'] = tokens[1]
        config['DEFAULT']['authorisation_token'] = tokens[0]
    return config


@pytest.mark.parametrize(('test_user_id', 'expected'), (
    (1070215, {
        'username': 'Serene-Arc',
        'id': 1070215,
        'professional': False,
        'country': 'au',
        'is_bot': False,
    }),
))
def test_get_user_data_from_id(test_user_id: int, expected: dict, config: ConfigParser):
    test_user = Player(config, 5)
    test_user.load_tokens()
    result = test_user.get_user_data_from_id(test_user_id)
    assert isinstance(result, dict)
    assert all([result.get(k) == expected[k] for k in expected.keys()])


@pytest.mark.parametrize(('test_user_id', 'expected_len_min'), (
    (1070215, 4),
))
def test_get_games_from_user_id(test_user_id: int, expected_len_min: int, config: ConfigParser):
    test_user = Player(config, 5)
    test_user.load_tokens()
    result = test_user.get_games_from_user_id(test_user_id)
    assert isinstance(result, dict)
    assert result.get('count') <= expected_len_min


@pytest.mark.parametrize(('test_username', 'expected'), (
    ('Serene-Arc', 1070215),
))
def test_resolve_username_to_id(test_username: str, expected: int, config: ConfigParser):
    test_user = Player(config, 5)
    test_user.load_tokens()
    result = test_user.resolve_username_to_id(test_username)
    assert result == expected


@pytest.mark.slow
@pytest.mark.parametrize(('test_user_id', 'expected_len', 'expected_files'), (
    (1070215, 4, {
        '40071592_teaching game 0002.sgf',
    }),
    ('21529', 80, {}),
))
def test_download_games_from_user_id(
        test_user_id: int,
        expected_len: int,
        tmp_path: Path,
        config: ConfigParser,
        expected_files: set[str],
):
    test_user = Player(config, 5)
    test_user.load_tokens()
    test_user.download_games_from_user_id(test_user_id, tmp_path, '{ID}_{NAME}')
    files = list(tmp_path.iterdir())
    assert len(files) == expected_len
    filenames = [f.name for f in files]
    assert all([n in filenames for n in expected_files])
