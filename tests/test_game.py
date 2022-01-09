#!/usr/bin/env python3
# coding=utf-8

from datetime import datetime

import pytest

from ogsdownloader.game import Game


@pytest.fixture(scope='function')
def test_data() -> dict:
    test_data = {
        'id': 123456,
        'name': 'test_game',
        'players': {
            'black': {'username': 'black_user'},
            'white': {'username': 'white_user'},
        },
        'started': datetime(2022, 1, 7, 8).isoformat(),
        'ended': datetime(2022, 1, 7, 9).isoformat(),
    }
    return test_data


def test_make_game(test_data: dict):
    result = Game(test_data)
    assert result.sgf_link == 'http://online-go.com/api/v1/games/123456/sgf/'


@pytest.mark.parametrize(('test_format_string', 'expected'), (
    ('{ID}', '123456.sgf'),
    ('{NAME}', 'test_game.sgf'),
    ('{BLACK} - {ID}', 'black_user - 123456.sgf'),
))
def test_game_format_name(test_format_string: str, expected: str, test_data: dict):
    test_game = Game(test_data)
    result = test_game.generate_filename(test_format_string)
    assert result == expected
