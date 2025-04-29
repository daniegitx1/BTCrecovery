import shlex
import subprocess
import re
from datetime import datetime
import sys

def run_seed_repair_command(command_str, raw_seed_phrase=None):
    try:
        # Split command string
        cleaned = re.sub(r'^python\s+seedrecover\.py\s*', '', command_str)
        cmd_parts = shlex.split(cleaned)
        cmd = [sys.executable, 'seedrecover.py'] + cmd_parts

        # Try to extract faulty seed
        faulty_list = []
        if '--mnemonic' in cmd_parts:
            try:
                idx = cmd_parts.index('--mnemonic')
                if idx + 1 < len(cmd_parts):
                    parsed_seed = cmd_parts[idx + 1].strip('"')
                    faulty_list = parsed_seed.split()
            except Exception:
                pass
        elif raw_seed_phrase:
            faulty_list = raw_seed_phrase.split()

        # Run the subprocess
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

        # Parse useful info
        match_line = None
        if "MATCHING SEED FOUND" in output:
            match_line = "MATCHING SEED FOUND!"
        elif "Seed found:" in output:
            match_line = "SEED FOUND"

        derivation_path = re.search(r"Matched on Address at derivation path: ([^\n]+)", output)
        seed_found = re.search(r"Seed found:\s+([a-z\s]+)", output)
        timestamp = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", output)

        return {
            'match_line': match_line,
            'derivation_path': derivation_path.group(1) if derivation_path else "",
            'timestamp': timestamp.group(1) if timestamp else datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'faulty_seed': " ".join(faulty_list) if faulty_list else None,
            'correct_seed': seed_found.group(1).strip() if seed_found else None,
            'raw_output': output,
        }

    except subprocess.CalledProcessError as e:
        return {
            'error': f"An error occurred during seed repair.\n\n{e.output}"
        }
    except Exception as ex:
        return {
            'error': f"Unexpected error: {str(ex)}"
        }
