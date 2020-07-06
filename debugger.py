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


def trace_lines(frame, event, arg):
    print(frame.f_lineno)


def debug(q):
    sys.settrace(trace_calls)
    sample(2, 3)
    while (True):
        c = q.get()
        if c == 'q':
            return
        print('in function', c)


breakpoints = {}
commands = Queue()
p = Process(target=debug, args=(commands,))
p.start()

for line in sys.stdin:
    command = line.split()

    if 'q' == command[0]:
        print('qutting debugger')
        commands.put('q')
        break

    if 'b' == command[0]:
        filename, line_no = command[1].split(':')
        breakpoints[f'{filename}:{line_no}'] = True
        print(f'breaking at {filename} {line_no}')
    if 'c' == command[0]:
        print('continuing execution')
        commands.put('c')
    if 's' == command[0]:
        print('stepping')
        commands.put('s')
