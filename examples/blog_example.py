import sys
import inspect
from types import FrameType

class Pydbg:

    def print_source(self, frame: FrameType):
        (fil, line, func, code, idx) = inspect.getframeinfo(frame)
        line = f'{fil}:{line}:{func}\n--> {code[idx]}'
        print(line)


    def trace_calls(self, frame: FrameType, _event, _arg):
        self.print_source(frame)
        return self.trace_calls


    def break_point(self):
        sys.settrace(self.trace_calls)

if __name__ == "__main__":
    pydbg = Pydbg()

    def factorial(n):
        if n == 0:
            return 1
        return n * factorial(n - 1)

    pydbg.break_point()
    print(factorial(3))
