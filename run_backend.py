#!/usr/bin/env python
import os
import sys
import subprocess

# Promijeni direktorij na backend
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.getcwd())

# Pokreni uvicorn
subprocess.run([sys.executable, '-m', 'uvicorn', 'app.main:app', '--reload', '--host', '127.0.0.1', '--port', '8000'])
