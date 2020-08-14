from unittest.mock import patch, call, Mock, MagicMock
from pydbg.debugger import dbg

import pytest

@patch('pydbg.debugger.inspect')
@patch('builtins.print')
def test_print_source(mocked_print, mocked_inspect):
    code = Mock(co_name='function_name', co_filename='file_name', co_firstlineno=2)
    frame = Mock(f_lineno=3, f_code=code)
    mocked_inspect.getsourcelines.return_value = (['one', 'two', 'three', 'four', 'five'], 9)
    dbg.print_source(frame)
    expected_output = '\x1b[34mfile_name:function_name:3\x1b[00m\n  one\n> two\n  three'
    assert mocked_print.mock_calls == [call(expected_output)]

@patch('builtins.print')
def test_prompt(mocked_print):
    dbg.prompt()
    assert mocked_print.mock_calls == [call('(pydbg)', end=' ', flush=True)]

@pytest.mark.parametrize(
    'command_input, result',
    [
        ('c', {'command': 'c'}),
        ('s', {'command': 's'}),
        ('n', {'command': 'n'}),
        ('f', {'command': 'f'}),
        ('b file_name:43', {'command': 'b', 'line': 'file_name:43'})
    ])


@patch('pydbg.debugger.sys')
def test_get_command(mocked_sys, command_input, result):
    mocked_sys.stdin = [command_input]
    assert dbg.get_command() == result


@pytest.fixture
def line():
    return 21

@pytest.fixture
def filename():
    return 'file_name'

@pytest.fixture
def frame(filename, line):
    f = Mock()
    f.f_code.co_filename = filename
    f.f_lineno = line
    return f


def test_location(frame, filename, line):
    assert dbg.get_location(frame) == f'{filename}:{line}'

