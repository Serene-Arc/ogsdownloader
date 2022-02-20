#!/usr/bin/env python3
# coding=utf-8
from argparse import ArgumentParser, Namespace
from pathlib import Path

import pytest
import shutil

import ogsdownloader.__main__ as main


@pytest.fixture()
def args(tmp_path: Path) -> Namespace:
    shutil.copy(Path('test_config.cfg'), Path(tmp_path, 'test_config.cfg'))
    parser = ArgumentParser()
    main.add_arguments(parser)
    args = parser.parse_args([f'-v', f'{tmp_path}', '-f{{ID}}', '-c', str(Path(tmp_path, 'test_config.cfg'))])
    return args


def test_integration_basic(args: Namespace, capsys: pytest.CaptureFixture):
    args.game = [41362224, ]
    main.main(args)
    output = capsys.readouterr()
    assert 'Wrote file to' in output.err


@pytest.mark.slow
def test_integration_user_profile(args: Namespace, capsys: pytest.CaptureFixture):
    args.user_id = ['1070215', ]
    main.main(args)
    output = capsys.readouterr()
    assert 'Wrote file to' in output.err


def test_integration_basic_authorised(args: Namespace, capsys: pytest.CaptureFixture):
    args.game = [41362224, ]
    args.authorised = True
    main.main(args)
    output = capsys.readouterr()
    assert 'Wrote file to' in output.err
