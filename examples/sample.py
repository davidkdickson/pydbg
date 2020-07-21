import pydbg.debugger

def inner():
    inner_x = 1
    inner_x += 2
    return inner_x


def sample(arg_a, arg_b):
    addition = arg_a + arg_b
    multiply = addition * arg_a * arg_b
    inner()
    sample_y = 1
    print('Sample: ' + str(multiply))
    sample_y += 2
    sample_y += 3


pydbg.break_point()
sample(4, 5)
