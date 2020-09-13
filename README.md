# Pydbg

Building a simple debugger in Python. Has the following commands:
* (s)tep in
* step over (n)
* step out (f)
* break at line number (b file:line_number) `(pydbg) b /home/david/Workspace/pydbg/examples/sample.py:10`
* (c)ontinue
* (q)uit

## Running examples
Example setting a breakpoint within a script using `pydbg.breakpoint()`.
```
python -m examples.sample
```
Enters debugger at start of script.
```
python -m pydbg examples/script.py
```

