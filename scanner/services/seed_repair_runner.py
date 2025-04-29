import os
import subprocess
import threading
import shlex
from subprocess import Popen
from typing import Optional

# ─────────────────────────────────────────────────────
# 📁 Path Configuration
# ─────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "runtime")
SEEDREPAIR_LOG_PATH = os.path.join(RUNTIME_DIR, "seedrepair_output.log")
DEBUG_LOG_PATH = os.path.join(RUNTIME_DIR, "error_debug.txt")

# ─────────────────────────────────────────────────────
# ⚙️ Process Handle
# ─────────────────────────────────────────────────────
ACTIVE_PROCESS: Optional[Popen] = None

# ─────────────────────────────────────────────────────
# 🛠️ Command Construction
# ─────────────────────────────────────────────────────
def build_recovery_command(script_path, args_string):
    python_executable = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
    args_list = shlex.split(args_string.strip())
    return [python_executable, script_path] + args_list

# ─────────────────────────────────────────────────────
# 📝 Command Logging
# ─────────────────────────────────────────────────────
def log_command_to_file(command_list):
    os.makedirs(os.path.dirname(SEEDREPAIR_LOG_PATH), exist_ok=True)
    with open(SEEDREPAIR_LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(" ".join(command_list) + "\n")

# ─────────────────────────────────────────────────────
# 🚀 Command Execution Thread
# ─────────────────────────────────────────────────────
def run_repair_command(command_list):
    def target():
        global ACTIVE_PROCESS

        # Clear old logs
        open(DEBUG_LOG_PATH, 'w').close()
        open(SEEDREPAIR_LOG_PATH, 'w').close()
        open(os.path.join(RUNTIME_DIR, "recovery_output.txt"), 'w').close()

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

                with open(SEEDREPAIR_LOG_PATH, 'a', encoding='utf-8') as log_file:
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
# ❌ Stop Running Recovery
# ─────────────────────────────────────────────────────
def stop_repair_command():
    global ACTIVE_PROCESS
    if ACTIVE_PROCESS and ACTIVE_PROCESS.poll() is None:
        ACTIVE_PROCESS.terminate()
        ACTIVE_PROCESS = None
        return True
    return False
