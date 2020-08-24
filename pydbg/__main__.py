import os
import runpy
import sys
import pydbg

path = os.path.abspath(sys.argv[1])

pydbg.debugger.dbg.set_module(path)
pydbg.break_point()

runpy.run_path(path)
