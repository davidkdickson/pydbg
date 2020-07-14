import sys
import inspect

breakpoints = {}
cmd = None

def print_source(frame):
    code = frame.f_code
    func_name = code.co_name
    line_no = frame.f_lineno
    filename = code.co_filename
    source = inspect.getsourcelines(code)[0]
    start_line = code.co_firstlineno
    print(f'{filename}:{func_name}:{line_no}')

    for index, source_line in enumerate(source, start=0):
        idx = line_no - start_line
        if idx == index:
            print('>', source_line.rstrip()[2:])
        if idx in [index - 1, index + 1] and index > 0:
            print(source_line.rstrip())


def prompt():
    print('(pydbg)', end=" ", flush=True)
    return


def get_command():
    prompt()
    line = input()
    command = line.split()

    if command[0] == 'q':
        print('qutting debugger')
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


def get_location(frame):
    code = frame.f_code
    func_name = code.co_name
    line_no = frame.f_lineno
    filename = code.co_filename
    return f'{filename}:{line_no}'


def trace_calls(frame, event, arg):
    global cmd
    global breakpoints

    # do not trace lines as previous command was (n)ext or (f)inish
    if event == 'call' and cmd in ['n', 'f']:
        return (cmd := None)

    if event == 'call' and cmd == 'c' and not breakpoints.get(get_location(frame), False):
        return continue_execution

    print_source(frame)

    command = get_command()
    cmd = command['command']

    while(cmd == 'b'):
        breakpoints[command['line']] = True
        command = get_command()
        cmd = command['command']

    if cmd in ['s', 'n']:
        return trace_lines

    if cmd == 'f':
        return (cmd := None)

    if cmd == 'c':
        return continue_execution

    raise 'unknown command'


def trace_lines(frame, event, arg):
    global cmd
    global breakpoints

    if event != 'line':
        return

    if cmd == 'c':
        return continue_execution

    print_source(frame)

    command = get_command()
    cmd = command['command']

    while(cmd == 'b'):
        breakpoints[command['line']] = True
        command = get_command()
        cmd = command['command']

    if cmd == 's':
        return trace_lines
    if cmd == 'n':
        return None
    if cmd == 'f':
        del frame.f_trace
        return None
    if cmd == 'c':
        return continue_execution

    raise 'unknown command'


def continue_execution(frame, event, arg):
    global cmd
    global breakpoints

    location = get_location(frame)

    if breakpoints.get(location, False):
        del breakpoints[location]
        print_source(frame)
        command = get_command()
        cmd = command['command']

        while(cmd == 'b'):
            breakpoints[command['line']] = True
            command = get_command()
            cmd = command['command']

        return trace_lines

    return continue_execution


def breakpoint():
    sys.settrace(trace_calls)


if (__name__ == '__main__'):
    pydbg()
