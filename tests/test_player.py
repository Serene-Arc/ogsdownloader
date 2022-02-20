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
    (1070215, 40),
))
def test_get_games_from_user_id(test_user_id: int, expected_len_min: int, config: ConfigParser):
    test_user = Player(config, 5)
    test_user.load_tokens()
    result = test_user.get_games_from_user_id(test_user_id)
    assert isinstance(result, list)
    assert len(result) >= expected_len_min


@pytest.mark.parametrize(('test_username', 'expected'), (
    ('Serene-Arc', 1070215),
))
def test_resolve_username_to_id(test_username: str, expected: int, config: ConfigParser):
    test_user = Player(config, 5)
    test_user.load_tokens()
    result = test_user.resolve_username_to_id(test_username)
    assert result == expected


@pytest.mark.parametrize(('test_game_id', 'expected'), (
    (41362224, {
        'black': 1070215,
        'rules': 'japanese',
        'white_lost': True,
    }),
))
def test_download_game_data_from_id(test_game_id: int, expected: dict, config: ConfigParser):
    test_user = Player(config, 5)
    test_user.load_tokens()
    result = test_user.get_game_data_from_id(test_game_id)
    assert all([result[key] == expected[key] for key in expected.keys()])
