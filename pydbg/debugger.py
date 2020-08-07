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
    def get_location(frame):
        return f'{frame.f_code.co_filename}:{frame.f_lineno}'

    def trace_calls(self, frame, event, _arg):
        # do not trace lines as previous command was (n)ext or (f)inish
        if event == 'call' and self.cmd in ['n', 'f']:
            self.cmd = None
            return None

        if self.cmd == 'c' and not self.breakpoints.get(self.get_location(frame), False):
            return self.continue_execution

        self.print_source(frame)

        command = self.get_command()
        self.cmd = command['command']

        while self.cmd == 'b':
            self.breakpoints[command['line']] = True
            command = self.get_command()
            self.cmd = command['command']

        if self.cmd in ['s', 'n']:
            return self.trace_calls

        if self.cmd == 'f':
            del frame.f_trace
            self.cmd = None
            return None

        if self.cmd == 'c':
            return self.continue_execution

        raise 'unknown command'

    def continue_execution(self, frame, _event, _arg):
        location = self.get_location(frame)

        if self.breakpoints.get(location, False):
            del self.breakpoints[location]
            self.print_source(frame)
            command = self.get_command()
            self.cmd = command['command']

            while self.cmd == 'b':
                self.breakpoints[command['line']] = True
                command = self.get_command()
                self.cmd = command['command']

            return self.trace_calls

        return self.continue_execution


def break_point():
    sys.settrace(dbg.trace_calls)


dbg = Pydbg()
