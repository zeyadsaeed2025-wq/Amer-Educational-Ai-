# Vercel API entry point
import os
import sys

# Determine the correct path to backend
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from 'api' to project root
backend_path = os.path.join(project_root, 'backend')

# Add backend to path
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Change to backend directory for relative imports
os.chdir(backend_path)

# Now import the app
from main import app as application

# Vercel requires the app to be named 'app'
app = application