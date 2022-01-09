#!/usr/bin/env python3
# coding=utf-8

import logging
import socket
from configparser import ConfigParser
from urllib.parse import urlencode

import requests
from requests import JSONDecodeError

from ogsdownloader.exceptions import AuthenticationError

logger = logging.getLogger(__name__)


def get_token(
        config: ConfigParser,
        refresh: bool = False,
) -> tuple[str, str]:
    data = {
        'client_id': config['DEFAULT']['client_id'],
        'client_secret': config['DEFAULT']['client_secret'],
        'username': config['DEFAULT']['username'],
    }
    if refresh:
        data.update({
            'refresh_token': config['DEFAULT']['refresh_token'],
            'grant_type': 'refresh_token',
        })
    else:
        data.update({
            'password': config['DEFAULT']['password'],
            'grant_type': 'password',
        })
    response = requests.post('https://online-go.com/oauth2/token/', data=data)
    try:
        response = response.json()
        return response['access_token'], response['refresh_token']
    except (JSONDecodeError, KeyError):
        logger.error('Failed to authenticate, did not receive a token')
        raise AuthenticationError()
