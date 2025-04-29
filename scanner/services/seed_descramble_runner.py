import os
import shlex
import subprocess
import re
from datetime import datetime
import sys

# Path setup
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
SEEDRECOVER_PATH = os.path.join(BASE_DIR, 'seedrecover.py')

def run_seed_descramble_command(command_str):
    try:
        cleaned = re.sub(r'^python\s+seedrecover\.py\s*', '', command_str)
        cmd_parts = shlex.split(cleaned)

        cmd = [sys.executable, SEEDRECOVER_PATH] + cmd_parts

        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True, cwd=BASE_DIR)

        match_line = None
        if "MATCHING SEED FOUND" in output:
            match_line = "MATCHING SEED FOUND!"
        elif "Seed found:" in output:
            match_line = "SEED FOUND"

        derivation_path = re.search(r"Matched on Address at derivation path: ([^\n]+)", output)
        seed_found_match = re.search(r"Seed found:\s+([a-z\s]+)", output)
        timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", output)

        return {
            'match_line': match_line,
            'derivation_path': derivation_path.group(1) if derivation_path else "",
            'timestamp': timestamp_match.group(1) if timestamp_match else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'correct_seed': seed_found_match.group(1).strip() if seed_found_match else "",
            'raw_output': output,
        }

    except subprocess.CalledProcessError as e:
        return {'error': f"An error occurred:\n{e.output}"}
