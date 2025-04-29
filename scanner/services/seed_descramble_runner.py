import os
import subprocess
import threading
import shlex
from subprocess import Popen
from typing import Optional

# ─────────────────────────────────────────────────────
# 📁 Paths
# ─────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "runtime")
DESCRAMBLE_LOG_PATH = os.path.join(RUNTIME_DIR, "descramble_output.log")
DEBUG_LOG_PATH = os.path.join(RUNTIME_DIR, "error_debug.txt")
RECOVERY_OUTPUT_PATH = os.path.join(RUNTIME_DIR, "recovery_output.txt")

# ─────────────────────────────────────────────────────
# 🚦 Global process tracker
# ─────────────────────────────────────────────────────

ACTIVE_PROCESS: Optional[Popen] = None

# ─────────────────────────────────────────────────────
# 🧱 Build Command
# ─────────────────────────────────────────────────────

def build_recovery_command(script_path: str, args_string: str) -> list[str]:
    python_exec = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
    args_list = shlex.split(args_string.strip())
    return [python_exec, script_path] + args_list

# ─────────────────────────────────────────────────────
# 🪵 Log Command
# ─────────────────────────────────────────────────────

def log_command_to_file(command_list: list[str]):
    os.makedirs(os.path.dirname(DESCRAMBLE_LOG_PATH), exist_ok=True)
    with open(DESCRAMBLE_LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(" ".join(command_list) + "\n")

# ─────────────────────────────────────────────────────
# ▶️ Run Process in Thread
# ─────────────────────────────────────────────────────

def run_descramble_command(command_list: list[str]):
    def target():
        global ACTIVE_PROCESS

        # Clear logs
        open(DEBUG_LOG_PATH, 'w').close()
        open(DESCRAMBLE_LOG_PATH, 'w').close()
        open(RECOVERY_OUTPUT_PATH, 'w').close()

        try:
            env = os.environ.copy()
            env['NO_PAUSE'] = '1'
            creation_flags = subprocess.CREATE_NO_WINDOW

            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as debug:
                debug.write("Launching command:\n")
                debug.write(" ".join(command_list) + "\n\n")
                debug.write("Working Directory:\n" + PROJECT_ROOT + "\n\n")

                ACTIVE_PROCESS = subprocess.Popen(
                    command_list,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=PROJECT_ROOT,
                    env=env,
                    creationflags=creation_flags,
                    text=True,
                    bufsize=1
                )

                debug.write("Process started successfully.\n\n")
                debug.flush()

                with open(DESCRAMBLE_LOG_PATH, 'a', encoding='utf-8') as log_file:
                    for line in iter(ACTIVE_PROCESS.stdout.readline, ''):
                        log_file.write(line)
                        log_file.flush()

                ACTIVE_PROCESS.wait()
                ACTIVE_PROCESS = None
                debug.write("Process finished.\n")

        except Exception as e:
            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as debug:
                debug.write(f"❌ Exception occurred:\n{str(e)}\n")

    thread = threading.Thread(target=target, daemon=True)
    thread.start()

# ─────────────────────────────────────────────────────
# ⛔ Stop Process
# ─────────────────────────────────────────────────────

def stop_descramble_command() -> bool:
    global ACTIVE_PROCESS
    if ACTIVE_PROCESS and ACTIVE_PROCESS.poll() is None:
        ACTIVE_PROCESS.terminate()
        ACTIVE_PROCESS = None
        return True
    return False
