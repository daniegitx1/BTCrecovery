
import os
import re
import shlex
from datetime import datetime
from scanner.arg_labels import ARG_LABELS

BASE_DIR = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(BASE_DIR, "runtime")

def parse_password_finder_output():
    result = _parse_common_output(
        log_file="descramble_output.log",
        toolset="Digital_Distillery|BTCrecovery|password_finder|btcrecover.py",
        arg_labels=ARG_LABELS
    )

    # Write Recovered_Key to recovery_output.txt if it exists
    if result.get("Recovered_Key"):
        try:
            with open(os.path.join(RUNTIME_DIR, "recovery_output.txt"), 'w', encoding='utf-8') as f:
                f.write(result["Recovered_Key"] + '\n')
        except Exception as e:
            result["Write_Error"] = f"Could not write output: {e}"

    return result


def parse_seed_repair_output():
    result = {}
    log_path = os.path.join(RUNTIME_DIR, "seedrepair_output.log")
    debug_path = os.path.join(RUNTIME_DIR, "error_debug.txt")
    output_path = os.path.join(RUNTIME_DIR, "recovery_output.txt")
    ts_path = os.path.join(RUNTIME_DIR, "timestamps.txt")

    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8') as f:
            result["Recovery_Log"] = f.read()

    if os.path.exists(output_path):
        with open(output_path, 'r', encoding='utf-8') as f:
            seed = f.read().strip()
            if seed:
                result["Recovered_Seed"] = seed
                result["Mnemonic"] = seed
            else:
                return {}

    if os.path.exists(debug_path):
        with open(debug_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                if "Launching command:" in line and i + 1 < len(lines):
                    result["Full_Command"] = lines[i + 1].strip()
                    break

    if "Recovery_Log" in result:
        if m := re.search(r"Starting (btcrecover.*?) on Python", result["Recovery_Log"]):
            result["Software_Version"] = m.group(1).strip()

    result["Toolset"] = "Digital_Distillery|BTCrecovery|seed_repair|seedrecover.py"

    _parse_command_line_args(result, ARG_LABELS)

    _parse_timestamps_from_file(result)

    return result

def parse_descramble_output():
    return _parse_common_output(
        log_file="descramble_output.log",
        toolset="Digital_Distillery|BTCrecovery|seed_descramble|seedrecover.py",
        arg_labels=ARG_LABELS
    )

def parse_recovery_output():
    result = _parse_common_output(
        log_file="descramble_output.log",
        toolset="Digital_Distillery|BTCrecovery|private_key_repair|btcrecover.py",
        arg_labels=ARG_LABELS
    )

    if result.get("Recovered_Key"):
        with open(os.path.join(RUNTIME_DIR, "recovery_output.txt"), 'w', encoding='utf-8') as f:
            f.write(result["Recovered_Key"] + '\n')

    return result

def parse_passphrase_output():
    result = _parse_common_output(
        log_file="descramble_output.log",
        toolset="Digital_Distillery|BTCrecovery|passphrase_finder|btcrecover.py",
        arg_labels=ARG_LABELS
    )

    if result.get("Recovered_Key"):
        with open(os.path.join(RUNTIME_DIR, "recovery_output.txt"), 'w', encoding='utf-8') as f:
            f.write(result["Recovered_Key"] + '\n')

    return result


def _parse_common_output(log_file, toolset, arg_labels):
    result = {}
    log_path = os.path.join(RUNTIME_DIR, log_file)
    debug_path = os.path.join(RUNTIME_DIR, "error_debug.txt")

    if not os.path.exists(log_path):
        return result

    with open(log_path, 'r', encoding='utf-8') as f:
        result["Recovery_Log"] = f.read()

    result["Toolset"] = toolset
    _parse_timestamps_from_file(result)

    if os.path.exists(debug_path):
        with open(debug_path, 'r', encoding='utf-8') as f:
            debug_lines = f.readlines()
            for i, line in enumerate(debug_lines):
                if "Launching command:" in line and i + 1 < len(debug_lines):
                    result["Full_Command"] = debug_lines[i + 1].strip()
                    break

    _parse_command_line_args(result, arg_labels)

    log = result.get("Recovery_Log", "")

    if m := re.search(r"Seed found:\s*(.+)", log):
        result["Recovered_Seed"] = m.group(1).strip()

    if m := re.search(r"Password found:\s*'(.+?)'", log):
        result["Recovered_Key"] = m.group(1).strip()

    if m := re.search(r"Matched on Address at derivation path:\s*(.+)", log):
        result["Matched_Derivation_Path"] = m.group(1).strip()

    if m := re.search(r"Starting (seedrecover|btcrecover).*? on Python", log):
        result["Software_Version"] = m.group(0).replace("Starting ", "").strip()

    return result

def _parse_timestamps_from_file(result):
    fmt = "%Y-%m-%d %H:%M:%S"
    start_time = None
    end_time = None
    ts_path = os.path.join(RUNTIME_DIR, "timestamps.txt")

    if os.path.exists(ts_path):
        try:
            with open(ts_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.startswith("Start_Time="):
                        start_time = datetime.fromisoformat(line.strip().split("=")[1])
                        result["Start_Time"] = start_time.strftime(fmt)
                    elif line.startswith("End_Time="):
                        end_time = datetime.fromisoformat(line.strip().split("=")[1])
                        result["End_Time"] = end_time.strftime(fmt)
        except Exception as e:
            print(f"⚠️ Failed to read timestamps.txt: {e}")

    if start_time and end_time:
        if end_time >= start_time:
            duration = end_time - start_time
            result["Recovery_Date"] = end_time.strftime("%d-%m-%Y")
            result["Total_Recovery_Time"] = str(duration).split('.')[0]
        else:
            result["Total_Recovery_Time"] = "Unknown"
    else:
        result["Total_Recovery_Time"] = "Unknown"

def _parse_command_line_args(result, arg_labels):
    try:
        tokens = shlex.split(result.get("Full_Command", ""), posix=False)
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
    except Exception as e:
        result["Parsed_Arguments"] = ""
        result["Error"] = f"Error parsing args: {str(e)}"
