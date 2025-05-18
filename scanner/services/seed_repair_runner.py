import os
import subprocess
import threading
import shlex
from subprocess import Popen
from typing import Optional
from datetime import datetime

# ─────────────────────────────────────────────────────
# 📁 Path Configuration
# ─────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "runtime")
SEEDREPAIR_LOG_PATH = os.path.join(RUNTIME_DIR, "seedrepair_output.log")
DEBUG_LOG_PATH = os.path.join(RUNTIME_DIR, "error_debug.txt")
OUTPUT_PATH = os.path.join(RUNTIME_DIR, "recovery_output.txt")
TIMESTAMPS_PATH = os.path.join(RUNTIME_DIR, "timestamps.txt")

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
        f.write(" ".join(shlex.quote(arg) for arg in command_list))

# ─────────────────────────────────────────────────────
# 🚀 Command Execution Thread
# ─────────────────────────────────────────────────────
def run(command_list):
    def target():
        global ACTIVE_PROCESS

        # Clear old logs
        for path in [DEBUG_LOG_PATH, SEEDREPAIR_LOG_PATH, OUTPUT_PATH, TIMESTAMPS_PATH]:
            open(path, 'w').close()

        start_time = None
        end_time = None

        try:
            env = os.environ.copy()
            env['NO_PAUSE'] = '1'
            creation_flags = subprocess.CREATE_NO_WINDOW
            print("🟢 Starting recovery thread...")
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

                with open(SEEDREPAIR_LOG_PATH, 'a', encoding='utf-8') as log_file:
                    for line in iter(ACTIVE_PROCESS.stdout.readline, ''):
                        log_file.write(line)
                        log_file.flush()

                ACTIVE_PROCESS.wait()
                print("🟢 Process wait completed.")
                ACTIVE_PROCESS = None

                end_time = datetime.now()

                with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as debug:
                    debug.write(f"\nEnd Time:\n{end_time.strftime('%Y-%m-%d %H:%M:%S.%f')}\n")
                    debug.write("Process finished.\n")

                # Normal timestamp save (inside try)
                with open(TIMESTAMPS_PATH, 'w', encoding='utf-8') as ts:
                    ts.write(f"Start_Time={start_time.isoformat()}\n")
                    ts.write(f"End_Time={end_time.isoformat()}\n")
                print(f"🟢 timestamps.txt written at {TIMESTAMPS_PATH}")

        except Exception as e:
            with open(DEBUG_LOG_PATH, 'a', encoding='utf-8') as debug:
                debug.write(f"❌ Exception occurred:\n{str(e)}\n")
            print(f"❌ Exception during recovery: {e}")

        finally:
            # Fallback timestamp save (in case above fails)
            if start_time and end_time:
                try:
                    with open(TIMESTAMPS_PATH, 'w', encoding='utf-8') as ts:
                        ts.write(f"Start_Time={start_time.isoformat()}\n")
                        ts.write(f"End_Time={end_time.isoformat()}\n")
                    print(f"✅ [finally] Timestamps saved: {start_time.isoformat()} to {end_time.isoformat()}")
                except Exception as e:
                    print(f"❌ Failed to write timestamps.txt in finally block: {e}")

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
