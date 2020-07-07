import sys
import inspect
from multiprocessing import Process, Queue


def inner():
    return 1


def sample(arg_a, arg_b):
    addition = arg_a + arg_b
    multiply = addition * arg_a * arg_b
    inner()
    print('Sample: ' + str(multiply))


def trace_calls(frame, event, arg):
    return trace_lines


breakpoints = {}
commands = Queue()


def trace_lines(frame, event, arg):
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

    print('(pydbg)', end=" ", flush=True)
    cmd = commands.get()

    if cmd == 's':
        return trace_lines

    if cmd == 'n':
        return trace_calls

    if cmd == 'q':
        raise 'stop execution'


def debug():
    sys.settrace(trace_calls)
    sample(2, 3)


p = Process(target=debug)
p.start()

for line in sys.stdin:
    command = line.split()
    if command[0] == 'q':
        print('qutting debugger')
        commands.put('q')
        break

    if command[0] == 'b':
        file, line = command[1].split(':')
        breakpoints[f'{file}:{line}'] = True
        print(f'breaking at {file} {line}')
    if command[0] == 'c':
        commands.put('c')
    if command[0] == 's':
        commands.put('s')
