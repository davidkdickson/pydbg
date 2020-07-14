import sys
import inspect

from color import Color


class Pydbg:
    def __init__(self):
        self.breakpoints = {}
        self.cmd = None


    def print_source(self, frame):
        code = frame.f_code
        func_name = code.co_name
        line_no = frame.f_lineno
        filename = code.co_filename
        source = inspect.getsourcelines(code)[0]
        start_line = code.co_firstlineno


        print(Color.BLUE.format(f'{filename}:{func_name}:{line_no}'))

        for index, source_line in enumerate(source, start=0):
            idx = line_no - start_line
            if idx == index:
                print('>', source_line.rstrip()[2:])
            if idx in [index - 1, index + 1] and index > 0:
                print(source_line.rstrip())


    def prompt(self):
        print('(pydbg)', end=" ", flush=True)


    def get_command(self):
        self.prompt()
        for line in sys.stdin:
            command = line.split()
            if not command:
                print(Color.RED.format('unknown command'))
                self.prompt()
                continue
            if command[0] == 'q':
                print(Color.RED.format('quitting debugger'))
                sys.exit(0)
            if command[0] == 'b':
                file, line = command[1].split(':')
                return {'command': 'b', 'line': f'{file}:{line}'}
            if command[0] == 'c':
                return {'command': 'c'}
            if command[0] == 's':
                return {'command': 's'}
            if command[0] == 'n':
                return {'command': 'n'}
            if command[0] == 'f':
                return {'command': 'f'}
            print(Color.RED.format('unknown command'))
            self.prompt()


    def get_location(self, frame):
        code = frame.f_code
        func_name = code.co_name
        line_no = frame.f_lineno
        filename = code.co_filename
        return f'{filename}:{line_no}'


    def trace_calls(self, frame, event, arg):

        # do not trace lines as previous command was (n)ext or (f)inish
        if event == 'call' and self.cmd in ['n', 'f']:
            self.cmd = None
            return None

        if event == 'call' and self.cmd == 'c' and not self.breakpoints.get(self.get_location(frame), False):
            return self.continue_execution

        self.print_source(frame)

        command = self.get_command()
        self.cmd = command['command']

        while(self.cmd == 'b'):
            self.breakpoints[command['line']] = True
            command = self.get_command()
            self.cmd = command['command']

        if self.cmd in ['s', 'n']:
            return self.trace_lines

        if self.cmd == 'f':
            return (cmd := None)

        if self.cmd == 'c':
            return self.continue_execution

        raise 'unknown command'


    def trace_lines(self, frame, event, arg):
        if event != 'line':
            return

        if self.cmd == 'c':
            return self.continue_execution

        self.print_source(frame)

        command = self.get_command()
        self.cmd = command['command']

        while(self.cmd == 'b'):
            self.breakpoints[command['line']] = True
            command = self.get_command()
            self.cmd = command['command']

        if self.cmd == 's':
            return self.trace_lines
        if self.cmd == 'n':
            return None
        if self.cmd == 'f':
            del frame.f_trace
            return None
        if self.cmd == 'c':
            return self.continue_execution

        raise 'unknown command'


    def continue_execution(self, frame, event, arg):
        location = self.get_location(frame)

        if self.breakpoints.get(location, False):
            del self.breakpoints[location]
            self.print_source(frame)
            command = self.get_command()
            self.cmd = command['command']

            while(cmd == 'b'):
                self.breakpoints[command['line']] = True
                command = self.get_command()
                self.cmd = command['command']

            return self.trace_lines

        return self.continue_execution



def breakpoint():
    dbg = Pydbg()
    sys.settrace(dbg.trace_calls)


