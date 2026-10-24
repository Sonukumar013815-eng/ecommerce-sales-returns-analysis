"""
E-Commerce Sales, Returns, and Customer Analysis Application.
Direct wrapper linking to dashboard.py.
"""
from pathlib import Path
import runpy

target_path = Path(__file__).resolve().parent / "dashboard.py"
runpy.run_path(str(target_path), run_name="__main__")
