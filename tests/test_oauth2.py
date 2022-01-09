#!/usr/bin/env python3
# coding=utf-8
from configparser import ConfigParser

import pytest

import ogsdownloader.oauth2 as oauth2


@pytest.fixture(scope='session')
def config() -> ConfigParser:
    config = ConfigParser()
    config.read('test_config.cfg')
    return config


def test_get_token(config: ConfigParser):
    result = oauth2.get_token(config)
    assert len(result) == 2
    assert all([isinstance(t, str) for t in result])
