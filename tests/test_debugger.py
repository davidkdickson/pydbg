from unittest.mock import patch, call, MagicMock, Mock
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

@patch('pydbg.debugger.inspect')
@patch('builtins.print')
def test_print_source(mocked_print, mocked_inspect):
    code = Mock(co_name='function_name', co_filename='file_name', co_firstlineno=2)
    frame = Mock(f_lineno=1, f_code=code)
    mocked_inspect.getsourcelines.return_value = (['this', 'is', 'code'], 9)
    dbg.print_source(frame)
    assert mocked_print.mock_calls == [call('\x1b[34mfile_name:function_name:1\x1b[00m')]
