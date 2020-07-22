from unittest.mock import patch, call
from pydbg.debugger import dbg

@patch('builtins.print')
def test_prompt(mocked_print):
    dbg.prompt()
    assert mocked_print.mock_calls == [call('(pydbg)', end=' ', flush=True)]
