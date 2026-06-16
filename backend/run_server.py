#!/usr/bin/env python
import sys
import os

# Add the backend directory to the Python path
backend_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, backend_dir)

# Set working directory to backend dir
os.chdir(backend_dir)

# Now run uvicorn
import uvicorn

if __name__ == "__main__":
    print(f"🚀 Starting backend from: {os.getcwd()}")
    print(f"   SQL database will be at: {os.getcwd()}/sql_app.db")
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)
