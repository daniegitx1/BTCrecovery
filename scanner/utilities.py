import os
import re
import shlex
from datetime import datetime
from scanner.arg_labels import ARG_LABELS

# ─────────────────────────────────────────────────────
# 📁 Path Configuration
# ─────────────────────────────────────────────────────

BASE_DIR = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(BASE_DIR, "runtime")

# ─────────────────────────────────────────────────────
# 🛠️ parse_seed_repair_output
# ─────────────────────────────────────────────────────

def parse_seed_repair_output():
    result = {}
    log_path = os.path.join(RUNTIME_DIR, "seedrepair_output.log")
    debug_path = os.path.join(RUNTIME_DIR, "error_debug.txt")
    output_path = os.path.join(RUNTIME_DIR, "recovery_output.txt")

    # Load log content
    log_content = ""
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            log_content = f.read()
            result["Recovery_Log"] = log_content

    # Extract recovered seed
    seed = ""
    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            seed = f.read().strip()

    if not seed:
        return {}

    result["Recovered_Seed"] = seed

    # Extract full command from error_debug.txt
    command_line = ""
    if os.path.exists(debug_path):
        with open(debug_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Launching command:" in line and i + 1 < len(lines):
                    command_line = lines[i + 1].strip()
                    result["Full_Command"] = command_line
                    break

    # Extract timestamps and software version
    if log_content:
        if m := re.search(r"Starting (btcrecover.*?) on Python", log_content):
            result["Software_Version"] = m.group(1).strip()

        timestamps = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", log_content)
        if timestamps:
            result["Start_Time"] = timestamps[0]
            result["End_Time"] = timestamps[-1]
            try:
                fmt = "%Y-%m-%d %H:%M:%S"
                start = datetime.strptime(timestamps[0], fmt)
                end = datetime.strptime(timestamps[-1], fmt)
                result["Total_Recovery_Time"] = str(end - start)
            except:
                result["Total_Recovery_Time"] = "Unknown"

    result["Toolset"] = "Digital_Distillery|BTCrecovery|seed_repair|seedrecover.py"

    # ───── Parse CLI Arguments ─────
    tokens = shlex.split(command_line)
    parsed_args = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token in ARG_LABELS:
            label = ARG_LABELS[token]
            if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                val = tokens[i + 1].strip()
                result[label] = val
                parsed_args.append(f"{label}: {val}")
                i += 1
            else:
                result[label] = "[on]"
                parsed_args.append(f"{label}: [on]")
        i += 1

    result["Parsed_Arguments"] = "\n".join(parsed_args)
    result["Mnemonic"] = result["Recovered_Seed"]  # 👈 Copy for display
    return result

# ─────────────────────────────────────────────────────
# 🧩 parse_descramble_output
# ─────────────────────────────────────────────────────

def parse_descramble_output():
    return _parse_common_output(
        log_file="descramble_output.log",
        toolset="Digital_Distillery|BTCrecovery|seed_descramble|seedrecover.py",
        arg_labels=ARG_LABELS
    )

# ─────────────────────────────────────────────────────
# 🔁 Shared Parsing Logic
# ─────────────────────────────────────────────────────

def _parse_common_output(log_file, toolset, arg_labels):
    result = {}
    log_path = os.path.join(RUNTIME_DIR, log_file)
    if not os.path.exists(log_path):
        return result

    with open(log_path, 'r', encoding='utf-8') as f:
        log_content = f.read()
        lines = log_content.splitlines()
        result["Recovery_Log"] = log_content

        if lines:
            command_line = lines[0].strip()
            result["Full_Command"] = command_line
        else:
            command_line = ""

        result["Toolset"] = toolset

        tokens = shlex.split(command_line)
        parsed_args = []
        i = 0
        while i < len(tokens):
            token = tokens[i]
            if token in arg_labels:
                label = arg_labels[token]
                if i + 1 < len(tokens) and not tokens[i + 1].startswith("--"):
                    val = tokens[i + 1].strip()
                    result[label] = val
                    parsed_args.append(f"{label}: {val}")
                    i += 1
                else:
                    result[label] = "[on]"
                    parsed_args.append(f"{label}: [on]")
            i += 1

        result["Parsed_Arguments"] = "\n".join(parsed_args)

        if m := re.search(r"Seed found:\s*(.+)", log_content):
            result["Recovered_Seed"] = m.group(1).strip()

        if m := re.search(r"Matched on Address at derivation path:\s*(.+)", log_content):
            result["Matched_Derivation_Path"] = m.group(1).strip()

        if m := re.search(r"Starting seedrecover (.*?) on Python", log_content):
            result["Software_Version"] = m.group(1).strip()

        timestamps = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", log_content)
        if timestamps:
            result["Start_Time"] = timestamps[0]
            result["End_Time"] = timestamps[-1]
            try:
                fmt = "%Y-%m-%d %H:%M:%S"
                start = datetime.strptime(timestamps[0], fmt)
                end = datetime.strptime(timestamps[-1], fmt)
                result["Recovery_Date"] = end.strftime("%d-%m-%Y")
                result["Total_Recovery_Time"] = str(end - start)
            except Exception:
                result["Total_Recovery_Time"] = "Unknown"

    return result
