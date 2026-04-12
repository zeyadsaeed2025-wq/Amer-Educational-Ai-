# Vercel API entry point - FastAPI on Vercel
import sys
import os

# Add backend to path
backend_dir = os.path.join(os.path.dirname(__file__), '..', 'backend')
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import the FastAPI app
from main import app

# Export for Vercel
# Vercel's Python runtime will use this as the ASGI app