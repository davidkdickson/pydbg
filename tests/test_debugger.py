from unittest.mock import patch, call, MagicMock
from pydbg.debugger import dbg

@patch('builtins.print')
def test_prompt(mocked_print):
    dbg.prompt()
    assert mocked_print.mock_calls == [call('(pydbg)', end=' ', flush=True)]

def test_location():
    frame = MagicMock()
    frame.f_code.co_filename = 'file'
    frame.f_lineno = 21
    assert dbg.get_location(frame) == 'file:21'

@patch('builtins.print')
@patch('inspect')
def test_print_source(mocked_print, mocked_inspect):
    inspect.getsourcelines
    frame = MagicMock()
    frame.code = "hello bob\nhello sam\nhello tim"
    frame.code.co_name = 'function'
    frame.f_lineno = 12
    frame.co_filename = 'file'

