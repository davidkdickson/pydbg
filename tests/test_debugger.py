from unittest.mock import patch, call, Mock
from pydbg.debugger import dbg

import pytest

@patch('pydbg.debugger.inspect')
@patch('builtins.print')
def test_print_source(mocked_print, mocked_inspect):
    code = Mock(co_name='function_name', co_filename='file_name')
    frame_mock = Mock(f_lineno=3, f_code=code)
    mocked_inspect.getsourcelines.return_value = (['one', 'two', 'three', 'four', 'five'], 9)
    dbg.print_source(frame_mock)
    expected_output = '\x1b[34mfile_name:function_name:3\x1b[00m\n  two\n> three\n  four'
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


@pytest.fixture(scope='module')
def line():
    return 21

@pytest.fixture(scope='module')
def filename():
    return 'file_name'

@pytest.fixture
def frame(filename, line):
    frame_mock = Mock()
    frame_mock.f_code.co_filename = filename
    frame_mock.f_lineno = line
    return frame_mock


def test_location(frame, filename, line):
    assert dbg.location(frame) == f'{filename}:{line}'

@pytest.mark.parametrize(
    'event, previous_command, trace_result',
    [
        ('return', None, dbg.trace_calls),
        ('call', 'n', None),
        ('call', 'f', None),
    ])
def test_trace_calls_event_check(frame, event, previous_command, trace_result):
    dbg.cmd = previous_command
    assert dbg.trace_calls(frame, event) == trace_result

def test_trace_calls_continue(frame):
    dbg.cmd = 'c'
    assert dbg.trace_calls(frame, 'line') == dbg.trace_calls

def test_trace_calls_breakpoint(frame):
    dbg.print_source = Mock()
    dbg.get_next_command = Mock()
    dbg.get_next_command.return_value = 's'
    dbg.breakpoints[dbg.location(frame)] = True
    assert dbg.trace_calls(frame, 'line') == dbg.trace_calls
    assert not dbg.breakpoints


def test_trace_calls_finish(frame):
    dbg.print_source = Mock()
    dbg.get_next_command = Mock()
    dbg.get_next_command.return_value = 'f'
    assert dbg.trace_calls(frame, 'line') == None


@pytest.mark.parametrize(
    'command, trace_result',
    [
        ('s', dbg.trace_calls),
        ('n', dbg.trace_calls),
        ('c', dbg.trace_calls),
    ])
def test_trace_calls(frame, command, trace_result):
    dbg.print_source = Mock()
    dbg.get_next_command = Mock()
    dbg.get_next_command.return_value = command
    assert dbg.trace_calls(frame, 'line') == trace_result


@patch('pydbg.debugger.inspect')
def test_trace_not_in_stack(mocked_inspect, frame):
    mocked_inspect.stack.return_value = [(1,1)]
    dbg.file = 'entry'
    assert dbg.trace_calls(frame, 'line') == None


def test_trace_not_at_entrypoint(frame):
    dbg.entrypoint = 'entrypoint'
    assert dbg.trace_calls(frame, 'line') == None


def test_trace_skip_module_load(frame):
    dbg.entrypoint = None
    dbg.file = None
    frame.f_code.co_name = '<module>'
    assert dbg.trace_calls(frame, 'call') == dbg.trace_calls

