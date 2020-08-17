import pydbg.debugger

x = 2

def testing():
    return 1

def inner():
    inner_x = 1
    inner_x += 2
    return inner_x


def sample(arg_a, arg_b):
    addition = arg_a + arg_b
    multiply = addition * arg_a * arg_b
    inner()
    pydbg.break_point()
    sample_y = 1
    print('Sample: ' + str(multiply))
    sample_y += 2
    sample_y += 3
    return 1

sample(4, 5)
