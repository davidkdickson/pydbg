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

def get_command():
    print('(pydbg)', end=" ", flush=True)
    return commands.get()

def trace_calls(frame, event, arg):
    print(f'trace_calls: {event}')
    return trace_lines


breakpoints = {}
commands = Queue()


def trace_lines(frame, event, arg):
    if event != 'line':
        print(f'trace_lines: {event}')
        return

    print_source(frame)

    cmd = get_command()

    if cmd == 's':
        return trace_lines
    if cmd == 'n':
        print('next')
        return trace_calls
    if cmd == 'f':
        del frame.f_trace
        return None

    raise 'unknown command'


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
        breakpoints[f'{file}:{line}'] = True
        print(f'breaking at {file} {line}')
    if command[0] == 'c':
        commands.put('c')
    if command[0] == 's':
        commands.put('s')
    if command[0] == 'n':
        commands.put('n')
    if command[0] == 'f':
        commands.put('f')
