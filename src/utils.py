import sys
import ctypes

def check_dependencies():
    """Verifies critical modules are installed."""
    try:
        import rich
        import questionary
    except ImportError as e:
        print(f"\033[91m[SYSTEM CRITICAL] MISSING MODULE: {e.name}\033[0m")
        print("Run: pip install -r requirements.txt")
        sys.exit(1)

def suppress_c_logs():
    """Silences Llama.cpp low-level C logging."""
    try:
        from llama_cpp import llama_log_set
        def null_log_callback(level, text, user_data): pass
        log_callback = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_char_p, ctypes.c_void_p)(null_log_callback)
        llama_log_set(log_callback, None)
    except: pass
