"""
Main entry point for QAEngineer Streamlit application.

Usage:
    streamlit run main.py
    # or
    python main.py
    # or
    streamlit run app/main.py
"""
import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Determine if executed within Streamlit runtime or via standard Python
def _is_streamlit_runtime() -> bool:
    try:
        from streamlit.runtime import exists  # type: ignore
        return exists()
    except Exception:
        pass
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx  # type: ignore
        return get_script_run_ctx() is not None
    except Exception:
        return False

def _find_python_interpreter() -> str:
    """Return python executable with streamlit installed, checking venvs if needed."""
    try:
        import streamlit  # type: ignore  # noqa: F401
        return sys.executable
    except ImportError:
        pass

    # Look for adjacent virtual environments
    candidates = [
        ROOT_DIR.parent / "AgentsVenv" / "Scripts" / "python.exe",
        ROOT_DIR / ".venv" / "Scripts" / "python.exe",
        ROOT_DIR / "venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    return sys.executable

if __name__ == "__main__":
    if _is_streamlit_runtime():
        import runpy
        app_path = ROOT_DIR / "app" / "main.py"
        runpy.run_path(str(app_path), run_name="__main__")
    else:
        import subprocess
        app_path = str(ROOT_DIR / "app" / "main.py")
        python_exe = _find_python_interpreter()
        cmd = [python_exe, "-m", "streamlit", "run", app_path] + sys.argv[1:]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass

