#!/usr/bin/env python3
# coding=utf-8
from argparse import ArgumentParser, Namespace
from pathlib import Path

import pytest

import ogsdownloader.__main__ as main


@pytest.fixture()
def args(tmp_path: Path) -> Namespace:
    parser = ArgumentParser()
    main.add_arguments(parser)
    args = parser.parse_args(f'-v {tmp_path} -f{{ID}} -ctest_config.cfg'.split(' '))
    return args


def test_integration_basic(args: Namespace, capsys: pytest.CaptureFixture):
    args.user_id = ['1070215', ]
    main.main(args)
    output = capsys.readouterr()
    assert 'Wrote file to' in output.err


def test_integration_basic_unauthorised(args: Namespace, capsys: pytest.CaptureFixture):
    args.user_id = ['1070215', ]
    args.unauthorised = True
    main.main(args)
    output = capsys.readouterr()
    assert 'Wrote file to' in output.err
