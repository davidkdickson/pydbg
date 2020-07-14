import debugger as dbg

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

dbg.breakpoint()
sample(4, 5)
