#!/usr/bin/env python3
# coding=utf-8

import argparse
import getpass
import logging
import sys
from configparser import ConfigParser
from pathlib import Path

import appdirs

from ogsdownloader import oauth2
from ogsdownloader.exceptions import AuthenticationError, OGSDownloaderException
from ogsdownloader.player import Player

parser = argparse.ArgumentParser()
logger = logging.getLogger()


def _setup_logging(verbosity: int):
    logger.setLevel(1)
    stream = logging.StreamHandler(sys.stderr)
    formatter = logging.Formatter('[%(asctime)s - %(name)s - %(levelname)s] - %(message)s')
    stream.setFormatter(formatter)
    logger.addHandler(stream)

    if verbosity > 0:
        stream.setLevel(logging.DEBUG)
    else:
        stream.setLevel(logging.INFO)

    logging.getLogger('urllib3').setLevel(logging.CRITICAL)


def add_arguments(parser: argparse.ArgumentParser):
    parser.add_argument('destination')
    parser.add_argument('--authorised', action='store_true')
    parser.add_argument('--username', default=None)
    parser.add_argument('-c', '--config', default=None)
    parser.add_argument('-f', '--format', type=str, default='{ID}')
    parser.add_argument('-i', '--interactive', action='store_true')
    parser.add_argument('-s', '--sleep', type=int, default=5)
    parser.add_argument('-u', '--user-id', action='append', default=[])
    parser.add_argument('-v', '--verbose', action='count', default=0)


def main(args: argparse.Namespace):
    _setup_logging(args.verbose)
    args.destination = Path(args.destination).expanduser().resolve()
    args.destination.mkdir(exist_ok=True, parents=True)
    config_directory = Path(appdirs.user_config_dir('ogsdownloader', 'serene-arc')).expanduser().resolve()
    if not config_directory.exists():
        config_directory.mkdir(parents=True, exist_ok=True)
    config = ConfigParser()
    if not args.config:
        config_file_location = Path(config_directory, 'config.cfg')
    else:
        args.config = Path(args.config).expanduser().resolve()
        config_file_location = args.config
    if config_file_location.exists():
        config.read(config_file_location)
    else:
        config_file_location.touch(exist_ok=True)

    if not config.has_option('DEFAULT', 'client_id'):
        config['DEFAULT']['client_id'] = 'bmATbhsh9RH7QXAR3n9Z88GBRoVqyxktj1RXcs9I'
    if not config.has_option('DEFAULT', 'client_secret'):
        config['DEFAULT']['client_secret'] = 'eAeq0D4CB9akF9WNpYZmYk8ZfrtpqfTV5TuerNa006dR5BdcYrMxnBPAN4Y2m9B4NR3DIT0'\
                                             'w3A1BqlJIOZXyIa8M32kIsg2q85HxsnWit5nYyHv9CeZafk5NLtww7iNq'

    if not config.has_option('DEFAULT', 'username') and not args.username and not args.unauthorised:
        if args.interactive:
            config['DEFAULT']['username'] = input('Pleas enter YOUR username: ')
        else:
            logger.error('Cannot proceed without a username to log in as')
            sys.exit(1)
    if all([
        not config.has_option('DEFAULT', 'refresh_token'),
        not config.has_option('DEFAULT', 'authorisation_token'),
        args.authorised,
    ]):
        if not config.has_option('DEFAULT', 'password'):
            config['DEFAULT']['password'] = getpass.getpass(
                f'Please enter OGS password for {config["DEFAULT"]["username"]}: ',
            )
        try:
            tokens = oauth2.get_token(config)
        except AuthenticationError:
            logger.critical(f'Could not authenticate with username and password provided')
        else:
            config.set('DEFAULT', 'refresh_token', tokens[1])
            config.set('DEFAULT', 'authorisation_token', tokens[0])

    player = Player(config, args.sleep)
    if not args.authorised:
        player.load_tokens()
        logger.debug('Tokens loaded')
    for user in args.user_id:
        try:
            user = int(user)
        except ValueError:
            try:
                user = player.resolve_username_to_id(user)
            except OGSDownloaderException as e:
                logger.error(e)
                continue

        player.download_games_from_user_id(user, args.destination, args.format)

    player.config.remove_option('DEFAULT', 'password')
    with open(config_file_location, 'w') as file:
        player.config.write(file)
    logger.debug(f'Update config file at {config_file_location}')


def entry():
    add_arguments(parser)
    args = parser.parse_args()
    main(args)


if __name__ == '__main__':
    entry()
