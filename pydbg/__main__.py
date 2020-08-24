import os
import runpy
import sys
import pydbg
path = os.path.abspath(sys.argv[1])
pydbg.debugger.dbg.entrypoint = path
pydbg.debugger.dbg.file = path
pydbg.break_point()
runpy.run_path(path)
