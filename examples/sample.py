import pydbg
import examples.sample_import as si

VARIABLE = 2

def testing():
    return 1

def inner():
    inner_x = 1
    inner_x += 2
    return inner_x


def function(arg_a, arg_b):
    addition = arg_a + arg_b
    multiply = addition * arg_a * arg_b
    pydbg.break_point()
    inner()
    sample_y = 1
    print('Sample: ' + str(multiply))
    import sys
    sys._current_frames()
    sample_y += 2
    sample_y += 3
    return 1

function(VARIABLE, 5)
si.hello()
