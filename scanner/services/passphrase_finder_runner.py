import os
import subprocess
import threading
import shlex
from subprocess import Popen
from typing import Optional
from datetime import datetime

# ─────────────────────────────────────────────────────
# 📁 Paths
# ─────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "runtime")
LOG_PATH = os.path.join(RUNTIME_DIR, "descramble_output.log")
DEBUG_LOG_PATH = os.path.join(RUNTIME_DIR, "error_debug.txt")
OUTPUT_PATH = os.path.join(RUNTIME_DIR, "recovery_output.txt")
TIMESTAMPS_PATH = os.path.join(RUNTIME_DIR, "timestamps.txt")

# ─────────────────────────────────────────────────────
# 🚦 Process Tracker
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
# 📜 Log Command
# ─────────────────────────────────────────────────────

def log_command_to_file(command_list: list[str]):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, 'w', encoding='utf-8') as f:
        f.write(" ".join(shlex.quote(arg) for arg in command_list) + "\n")

# ─────────────────────────────────────────────────────
# ▶️ Run Recovery Command
# ─────────────────────────────────────────────────────

def run(command_list: list[str]):
    def target():
        global ACTIVE_PROCESS
        start_time = None
        end_time = None

        # Clear all logs/output
        for path in [DEBUG_LOG_PATH, LOG_PATH, OUTPUT_PATH, TIMESTAMPS_PATH]:
            open(path, 'w').close()

        try:
            env = os.environ.copy()
            env['NO_PAUSE'] = '1'
            creation_flags = subprocess.CREATE_NO_WINDOW

            start_time = datetime.now()

            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as debug:
                debug.write("Launching command:\n")
                debug.write(" ".join(command_list) + "\n\n")
                debug.write("Working Directory:\n" + PROJECT_ROOT + "\n\n")
                debug.write(f"Start Time:\n{start_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n\n")

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

                with open(LOG_PATH, 'a', encoding='utf-8') as log_file:
                    for line in iter(ACTIVE_PROCESS.stdout.readline, ''):
                        log_file.write(line)
                        log_file.flush()

                ACTIVE_PROCESS.wait()
                end_time = datetime.now()
                ACTIVE_PROCESS = None

                debug.write(f"\nEnd Time:\n{end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
                debug.write("Process finished.\n")

                with open(TIMESTAMPS_PATH, 'w', encoding='utf-8') as ts:
                    ts.write(f"Start_Time={start_time.isoformat()}\n")
                    ts.write(f"End_Time={end_time.isoformat()}\n")

                print(f"✅ [passphrase_finder_runner] timestamps.txt written")

        except Exception as e:
            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as debug:
                debug.write(f"❌ Exception occurred:\n{str(e)}\n")
            print(f"❌ Exception in runner: {e}")

    thread = threading.Thread(target=target, daemon=True)
    thread.start()

# ─────────────────────────────────────────────────────
# 🛑 Stop Recovery
# ─────────────────────────────────────────────────────

def stop_recovery_command() -> bool:
    global ACTIVE_PROCESS
    if ACTIVE_PROCESS and ACTIVE_PROCESS.poll() is None:
        ACTIVE_PROCESS.terminate()
        ACTIVE_PROCESS = None
        return True
    return False
