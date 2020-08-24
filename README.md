# Pydbg

Building a simple debugger in Python. MVP should have the following commands:
* step in (done)
* step over (done)
* step out (done)
* break at line number (done)
* continue (done)
* quit (done)

## Running examples
Example setting a breakpoint within a script using `pydbg.breakpoint()`.
```
python -m examples.sample
```
Enters debugger at start of script.
```
python -m pydbg examples/script.py
```
