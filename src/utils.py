import sys

def check_dependencies():
    """Verifies critical modules are installed."""
    try:
        import rich
        import questionary
        import llama_cpp
        import numpy
    except ImportError as e:
        print(f"\033[91m[SYSTEM CRITICAL] MISSING MODULE: {e.name}\033[0m")
        print("Run: pip install rich questionary llama-cpp-python numpy")
        sys.exit(1)

def suppress_c_logs():
    """
    STUB: Log suppression via ctypes is disabled for Android/Termux stability.
    Attempting to silence C++ logs on this architecture causes Segfaults.
    """
    pass

