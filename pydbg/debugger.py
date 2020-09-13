import sys
import inspect

from types import FrameType
from typing import Dict

from pydbg import color

class Pydbg:
    def __init__(self):
        self.breakpoints = {}
        self.cmd = None
        self.entrypoint = None
        self.file = None


    @staticmethod
    def print_source(frame: FrameType) -> None:
        code = frame.f_code
        current_line = frame.f_lineno
        func_name = code.co_name
        filename = code.co_filename
        module = inspect.getmodule(code)

        if not module:
            return

        source = inspect.getsourcelines(module)[0]
        output = color.BLUE.format(f'{filename}:{func_name}:{current_line}')

        if (current_line - 2) >= 0:
            output += f'\n  {source[current_line - 2].rstrip()}'

        output += f'\n> {source[current_line - 1].rstrip()}'

        if current_line < len(source):
            output += f'\n  {source[current_line].rstrip()}'

        print(output)


    @staticmethod
    def prompt() -> None:
        print('(pydbg)', end=" ", flush=True)


    def set_module(self, path: str) -> None:
        self.entrypoint = path
        self.file = path


    def get_command(self) -> Dict[str, str]:
        self.prompt()
        command_hash = {'command': 'q'}

        for line in sys.stdin:
            command = line.split()
            if not command:
                print(color.RED.format('unknown command'))
                self.prompt()
                continue
            if command[0] == 'q':
                command_hash = {'command': 'q'}
                break
            if command[0] == 'b':
                file, line = command[1].split(':')
                command_hash = {'command': 'b', 'line': f'{file}:{line}'}
                break
            if command[0] == 'c':
                command_hash = {'command': 'c'}
                break
            if command[0] == 's':
                command_hash = {'command': 's'}
                break
            if command[0] == 'n':
                command_hash = {'command': 'n'}
                break
            if command[0] == 'f':
                command_hash = {'command': 'f'}
                break
            print(color.RED.format('unknown command'))
            self.prompt()
        return command_hash


    @staticmethod
    def location(frame: FrameType) -> str:
        return f'{frame.f_code.co_filename}:{frame.f_lineno}'


    def get_next_command(self) -> str:
        # loop while breakpoints are being set
        while (command := self.get_command()) == 'b':
            self.breakpoints[command['line']] = True

        return command['command']


    def trace_calls(self, frame, event, _arg=None):
        # clear once hit module entrypoint
        if frame.f_code.co_filename == self.entrypoint:
            self.entrypoint = None

        # ignore when at start or end of importing module when in script mode
        if self.entrypoint or (self.file and self.file not in map(lambda t: t[1], inspect.stack())):
            return None

        # without check repeats on return statement and entering a module using script mode
        if (frame.f_code.co_name == '<module>' and event == 'call') or event == 'return':
            return self.trace_calls

        # function call and previous command was (n)ext or (f)inish so do not trace lines
        if event == 'call' and self.cmd in ['n', 'f']:
            self.cmd = None
            return None

        # (c)ontinue until a breakpoint is reached
        if self.cmd == 'c':
            location = self.location(frame)
            if self.breakpoints.get(location, False):
                del self.breakpoints[location]
                self.cmd = None
            else:
                return self.trace_calls

        self.print_source(frame)
        self.cmd = self.get_next_command()

        if self.cmd == 'q':
            print(color.RED.format('quitting debugger'))
            sys.exit(0)

        if self.cmd in ['s', 'n', 'c']:
            return self.trace_calls

        # stepping out therefore delete trace function and continue
        if self.cmd == 'f':
            del frame.f_trace
            return None

        raise 'unknown command'


def break_point():
    # start tracing current frame
    previous_frame = inspect.currentframe().f_back
    module = inspect.getmodule(previous_frame)
    previous_frame.f_trace = dbg.trace_calls

    # trace all frames up the stack
    while inspect.getmodule(previous_frame.f_back) == module:
        previous_frame = previous_frame.f_back
        previous_frame.f_trace = dbg.trace_calls

    # trace subsequent frames
    sys.settrace(dbg.trace_calls)


dbg = Pydbg()
