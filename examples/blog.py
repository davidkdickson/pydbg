import sys
import inspect

class Pydbg:

    def print_source(self, frame, event, arg):
        (fil, line, func, code, idx) = inspect.getframeinfo(frame)
        line = f'{fil}:{line}:{func}\n--> {code[idx]}'
        print(line)

    def get_command(self):
        return 's'


    def trace_calls(self, frame, event, arg):
        self.print_source(frame, event, arg)
        self.cmd = self.get_command()

        if self.cmd == 's':
            return self.trace_calls

        self.print_source(frame, event, arg)

        raise 'Unknown command'


    def break_point(self):
        sys.settrace(self.trace_calls)



if __name__ == "__main__":
    pydbg = Pydbg()

    def fibonacci(n):
        if n in [0, 1]:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)


    pydbg.break_point()
    fibonacci(2)
