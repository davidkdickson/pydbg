import sys
import inspect
from types import FrameType

class Pydbg:

    def print_source(self, frame: FrameType):
        (fil, line, func, code, idx) = inspect.getframeinfo(frame)
        line = f'{fil}:{line}:{func}\n--> {code[idx]}'
        print(line)


    def get_command(self):
        return 's'


    def trace_calls(self, frame: FrameType, _event, _arg):
        self.print_source(frame)
        self.cmd = self.get_command()

        if self.cmd == 's':
            return self.trace_calls


        raise 'Unknown command'


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
