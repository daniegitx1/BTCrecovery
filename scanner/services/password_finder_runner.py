import os
import subprocess
import threading
import shlex

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
PYTHON_EXEC = os.path.join(PROJECT_ROOT, ".venv", "Scripts", "python.exe")
SCRIPT_PATH = os.path.join(PROJECT_ROOT, "btcrecover.py")
LOG_PATH = os.path.join(PROJECT_ROOT, "runtime", "descramble_output.log")
ERROR_LOG = os.path.join(PROJECT_ROOT, "runtime", "error_debug.txt")

ACTIVE_PROCESS = None

def run(args_string):
    global ACTIVE_PROCESS

    def target():
        try:
            open(LOG_PATH, 'w').close()
            open(ERROR_LOG, 'w').close()

            cmd = [PYTHON_EXEC, SCRIPT_PATH] + shlex.split(args_string, posix=False)

            with open(ERROR_LOG, 'a', encoding='utf-8') as err:
                err.write("Launching command:\n")
                err.write(" ".join(cmd) + "\n")

            with open(LOG_PATH, 'a', encoding='utf-8') as out:
                ACTIVE_PROCESS = subprocess.Popen(
                    cmd,
                    stdout=out,
                    stderr=subprocess.STDOUT,
                    cwd=PROJECT_ROOT,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                ACTIVE_PROCESS.wait()
        except Exception as e:
            with open(ERROR_LOG, 'a', encoding='utf-8') as err:
                err.write(f"Exception: {str(e)}\n")

    thread = threading.Thread(target=target)
    thread.start()


def stop():
    global ACTIVE_PROCESS
    if ACTIVE_PROCESS and ACTIVE_PROCESS.poll() is None:
        ACTIVE_PROCESS.terminate()
        ACTIVE_PROCESS = None


def check_finished():
    return ACTIVE_PROCESS is None or ACTIVE_PROCESS.poll() is not None
