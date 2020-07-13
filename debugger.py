import sys
import inspect
from multiprocessing import Process, Queue


def inner():
    x = 1 + 2
    y = 2 + x
    return y


def sample(arg_a, arg_b):
    addition = arg_a + arg_b
    multiply = addition * arg_a * arg_b
    inner()
    y = 100 + 200
    print('Sample: ' + str(multiply))
    y = 200
    y = 300


breakpoints = {}
commands = Queue()
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
    return commands.get()


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


def debug():
    sys.settrace(trace_calls)
    sample(2, 3)


p = Process(target=debug)
p.start()

for line in sys.stdin:
    command = line.split()
    if command[0] == 'q':
        print('qutting debugger')
        p.terminate()
        break
    if command[0] == 'b':
        file, line = command[1].split(':')
        commands.put({'command': 'b', 'line': f'{file}:{line}'})
    if command[0] == 'c':
        commands.put({'command': 'c'})
    if command[0] == 's':
        commands.put({'command': 's'})
    if command[0] == 'n':
        commands.put({'command': 'n'})
    if command[0] == 'f':
        commands.put({'command': 'f'})
