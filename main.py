# main.py (project root)
"""
Compatibility entrypoint for tests that import `from main import app`.
This simply re-exports the FastAPI app defined in backend.main.
"""
from backend.main import app  # noqa: F401
