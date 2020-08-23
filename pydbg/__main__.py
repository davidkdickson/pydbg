import os
import runpy
import sys
import pydbg
path = os.path.abspath(sys.argv[1])
pydbg.debugger.dbg.entrypoint = path
sys.settrace(pydbg.debugger.dbg.trace_calls)
runpy.run_path(path)
