#!/usr/bin/env python3
# coding=utf-8
import re
from datetime import datetime


class Game:
    def __init__(self, game_data: dict):
        self.data = game_data
        self.name: str = game_data['name']
        self.black = game_data['players']['black']['username']
        self.white = game_data['players']['white']['username']
        self.game_id: int = game_data['id']
        self.sgf_link: str = f'http://online-go.com/api/v1/games/{game_data["id"]}/sgf/'
        self.start_time = datetime.fromisoformat(game_data['started'])
        if game_data['ended']:
            self.end_time = datetime.fromisoformat(game_data['ended'])
        else:
            self.end_time = 'Unknown'

    def generate_filename(self, format_string: str) -> str:
        replacement_dict = {
            'NAME': self.name,
            'ID': self.game_id,
            'START': self.start_time.isoformat(),
            'END': self.end_time.isoformat() if isinstance(self.end_time, datetime) else self.end_time,
            'BLACK': self.black,
            'WHITE': self.white,
        }
        result = format_string
        for key in replacement_dict.keys():
            if re.search(fr'(?i).*{{{key}}}.*', result):
                result = re.sub(fr'(?i){{{key}}}', str(replacement_dict[key]), result)
        return result + '.sgf'
