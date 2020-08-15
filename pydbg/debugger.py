import sys
import inspect

from pydbg import color

class Pydbg:
    def __init__(self):
        self.breakpoints = {}
        self.cmd = None


    @staticmethod
    def print_source(frame):
        code = frame.f_code
        current_line = frame.f_lineno
        func_name = code.co_name
        filename = code.co_filename
        first_line = code.co_firstlineno
        source = inspect.getsourcelines(code)[0]
        output = color.BLUE.format(f'{filename}:{func_name}:{current_line}')

        idx = current_line - first_line

        if idx == 0:
            output += f'\n> {source[0].rstrip()}'
            output += f'\n  {source[1].rstrip()}'
            if len(source) > 2:
                output += f'\n  {source[2].rstrip()}'
        else:
            output += f'\n  {source[idx - 1].rstrip()}'
            output += f'\n> {source[idx].rstrip()}'
            if len(source) > (idx + 1):
                output += f'\n  {source[idx + 1].rstrip()}'

        print(output)


    @staticmethod
    def prompt():
        print('(pydbg)', end=" ", flush=True)


    def get_command(self):
        self.prompt()
        command_hash = None
        for line in sys.stdin:
            command = line.split()
            if not command:
                print(color.RED.format('unknown command'))
                self.prompt()
                continue
            if command[0] == 'q':
                print(color.RED.format('quitting debugger'))
                sys.exit(0)
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
    def location(frame):
        return f'{frame.f_code.co_filename}:{frame.f_lineno}'

    def get_next_command(self):
        # loop while breakpoints are being set
        while (command := self.get_command())['command'] == 'b':
            self.breakpoints[command['line']] = True

        return command['command']


    def trace_calls(self, frame, event, _arg=None):
        # without checking for this, repeats on return statement
        if event == 'return':
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

        if self.cmd in ['s', 'n', 'c']:
            return self.trace_calls

        # stepping out therefore delete trace function and continue
        if self.cmd == 'f':
            del frame.f_trace
            return None

        raise 'unknown command'


def break_point():
    sys.settrace(dbg.trace_calls)


dbg = Pydbg()
