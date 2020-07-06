import sys
from multiprocessing import Process, Queue


def sample(a, b):
    x = a + b
    y = x * 2
    print('Sample: ' + str(y))


def trace_calls(frame, event, arg):
    if frame.f_code.co_name == "sample":
        print(frame.f_code)
        return trace_lines
    return


breakpoints = {}
commands = Queue()


def trace_lines(frame, event, arg):
    print(frame.f_lineno)
    cmd = commands.get()
    if cmd == 's':
        return trace_lines

    if cmd == 'n':
        return trace_calls

    if cmd == 'q':
        raise 'stop execution'


def debug(q):
    sys.settrace(trace_calls)
    sample(2, 3)


p = Process(target=debug, args=(commands,))
p.start()

for line in sys.stdin:
    command = line.split()

    if command[0] == 'q':
        print('qutting debugger')
        commands.put('q')
        break

    if command[0] == 'b':
        filename, line_no = command[1].split(':')
        breakpoints[f'{filename}:{line_no}'] = True
        print(f'breaking at {filename} {line_no}')
    if command[0] == 'c':
        print('continuing execution')
        commands.put('c')
    if command[0] == 's':
        print('stepping')
        commands.put('s')
