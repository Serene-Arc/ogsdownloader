#!/usr/bin/env python3
# coding=utf-8

import json
import logging
import time
from configparser import ConfigParser
from json import JSONDecodeError
from pathlib import Path
from typing import Optional

import requests
from requests import Response

from ogsdownloader import oauth2
from ogsdownloader.exceptions import OGSDownloaderException
from ogsdownloader.game import Game

logger = logging.getLogger(__name__)


class Player:
    def __init__(self, config: ConfigParser, sleep: int):
        self.authorisation_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.config = config
        self.sleep_time = sleep

    def load_tokens(self):
        self.refresh_token = self.config['DEFAULT']['refresh_token']
        self.authorisation_token = self.config['DEFAULT']['authorisation_token']

    def get_user_data_from_id(self, user_id: int) -> dict:
        response = self.make_request(f'http://online-go.com/api/v1/players/{user_id}/')
        try:
            return response.json()
        except JSONDecodeError:
            raise

    def resolve_username_to_id(self, username: str) -> int:
        response = self.make_request(f'http://online-go.com/api/v1/players?username={username}')
        try:
            result = response.json()
            return result['results'][0].get('id')
        except JSONDecodeError:
            raise
        except KeyError:
            raise OGSDownloaderException(f'No user found to match username {username}')

    def get_games_from_user_id(self, user_id: int) -> list[dict]:
        results = []
        url = f'http://online-go.com/api/v1/players/{user_id}/games?page_size=50'
        while True:
            logger.debug(f'Requesting page {url} to get game data')
            response = self.make_request(url)
            try:
                game_data = response.json()
            except JSONDecodeError:
                raise
            results.extend(game_data['results'])
            if not game_data.get('next'):
                break
            else:
                url = game_data['next']
                time.sleep(self.sleep_time)
        return results

    def download_games_from_user_id(self, user_id: int, destination: Path, format_string: str):
        data = self.get_games_from_user_id(user_id)
        logger.debug(f'Found details of {len(data)} games')
        games = [Game(d) for d in data]
        logger.info(f'Found {len(games)} games for user id {user_id}')
        for g in games:
            sgf_file = self.make_request(g.sgf_link)
            file_path = Path(destination, g.generate_filename(format_string))
            with open(file_path, 'wb') as file:
                file.write(sgf_file.content)
            logger.info(f'Wrote file to {file_path}')
            time.sleep(self.sleep_time)

    def make_request(self, url: str) -> Response:
        headers = {
            'accept': 'application/json, application/x-go-sgf',
            'headers': 'Mozilla/5.0 (X11; Linux x86_64; rv:95.0) Gecko/20100101 Firefox/95.0',
            'Authorization': f'Bearer {self.authorisation_token}',
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            new_tokens = oauth2.get_token(self.config, True)
            self.refresh_token = new_tokens[1]
            self.authorisation_token = new_tokens[0]
            headers['Authorization'] = f'Bearer {self.authorisation_token}'
            response = requests.get(url, headers=headers)
            if response != 200:
                raise OGSDownloaderException(f'Failed to get {url}; status code {response.status_code}')
        return response
