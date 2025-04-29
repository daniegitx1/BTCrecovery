# scanner/views/seed_descramble.py
# scanner/views/seed_descramble.py

import os
import shlex
import subprocess
import sys
import time
import threading
import re

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from scanner.forms.seed_descramble import SeedDescrambleForm
from scanner.services.seed_descramble_runner import run_seed_descramble_command

def build_recovery_command(script_path, args_string):
    """
    Build the correct command list for launching recovery scripts.
    Automatically adds --nogui if needed.
    """
    base_cmd = [sys.executable, script_path]
    args_list = shlex.split(args_string)

    if os.path.basename(script_path).lower() == "btcrecover.py":
        if "--nogui" not in args_list:
            args_list.insert(0, "--nogui")  # Ensure --nogui is added FIRST after script
    return base_cmd + args_list

def parse_recovery_data():
    """
    Parses recovery_command.txt and full_recovery.log into structured readable information.
    """
    recovery_data = {}

    # Paths
    command_file = os.path.join(BASE_DIR, 'recovery_command.txt')
    log_file = os.path.join(BASE_DIR, 'full_recovery.log')

    # Parse recovery_command.txt
    if os.path.exists(command_file):
        with open(command_file, 'r', encoding='utf-8') as f:
            command_content = f.read()
        recovery_data['Full_Command'] = command_content

        # Updated argument translations
        arg_translations = {
            '--wallet-type': 'Wallet Type',
            '--addrs': 'Addresses',
            '--addr-limit': 'Address Limit',
            '--language': 'Language',
            '--mnemonic-length': 'Mnemonic Length',
            '--tokenlist': 'Wordlist File',
            '--dsw': 'Allow Word Swaps',
            '--no-dupchecks': 'Disable Duplicate Checking',
            '--no-eta': 'Suppress ETA',
            '--coin': 'Coin (Derivation)',
            '--bip32-path': 'Custom Derivation Path',
        }
        for arg, readable in arg_translations.items():
            if arg in command_content:
                parts = command_content.split(arg)
                if len(parts) > 1:
                    value = parts[1].split()[0]
                    recovery_data[readable] = value

    # Parse full_recovery.log
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            log_content = f.read()
        recovery_data['Full_Log'] = log_content

        # Simple parsing
        if "Seed found:" in log_content:
            match = re.search(r"Seed found:\s*(.*)", log_content)
            if match:
                recovery_data['Recovered_Seed'] = match.group(1).strip()

        if "Starting seedrecover" in log_content:
            start_match = re.search(r"Starting (.*?) on Python", log_content)
            if start_match:
                recovery_data['Software_Version'] = start_match.group(1).strip()

        # Timestamps
        timestamps = re.findall(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", log_content)
        if timestamps:
            recovery_data['Start_Time'] = timestamps[0]
            recovery_data['End_Time'] = timestamps[-1]

    return recovery_data


# Globals
current_process = None
last_recovery_result = None
process_start_time = None
full_recovery_log = None
logfile_writer_thread = None

# Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
SEEDRECOVER_PATH = os.path.join(BASE_DIR, "seedrecover.py")
LIST_FOLDER = os.path.join(BASE_DIR, "btcrecover", "dd-lists")
DERIVATION_FOLDER = os.path.join(BASE_DIR, "derivationpath-lists")


def input_view(request):
    return render(request, 'scanner/seed_descramble_input.html', {
        'form': SeedDescrambleForm()
    })


def result_view(request):
    global last_recovery_result
    if request.method == 'POST':
        constructed_string = request.POST.get('constructed_string', '').strip()
        if not constructed_string:
            return redirect('seed_descramble_input')
        context = run_seed_descramble_command(constructed_string)
        last_recovery_result = context
        return render(request, 'scanner/seed_descramble_result.html', context)
    elif last_recovery_result:
        context = last_recovery_result
        last_recovery_result = None
        return render(request, 'scanner/seed_descramble_result.html', context)
    else:
        return redirect('seed_descramble_input')


def start_recovery(request):
    global current_process, process_start_time, full_recovery_log, logfile_writer_thread

    args = request.GET.get('args', '')
    if not args:
        return JsonResponse({'success': False, 'error': 'No arguments provided.'})

    cmd = build_recovery_command(SEEDRECOVER_PATH, args)

    # Save full recovery command to recovery_command.txt
    full_recovery_command = " ".join(cmd)  # turn list into single string
    recovery_command_path = os.path.join(BASE_DIR, 'recovery_command.txt')

    try:
        with open(recovery_command_path, 'w', encoding='utf-8') as f:
            f.write(full_recovery_command)
        print(f"✅ Saved recovery command to {recovery_command_path}")
    except Exception as e:
        print(f"❌ Failed to save recovery command: {e}")

    print("\n🚀 Attempting to start recovery")
    print(f"🔹 BASE DIR: {BASE_DIR}")
    print(f"🔹 Working Directory: {BASE_DIR}")
    print(f"🔹 Python Executable: {sys.executable}")
    print(f"🔹 Full Command: {cmd}\n")

    env = os.environ.copy()
    env['FORCE_NO_GUI'] = '1'
    env['NO_PAUSE'] = '1'

    CREATE_NO_WINDOW = 0x08000000  # Suppress Windows console popup

    full_recovery_log = os.path.join(BASE_DIR, 'full_recovery.log')

    try:
        # Start process with PIPE
        current_process = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=BASE_DIR,
            env=env,
            creationflags=CREATE_NO_WINDOW,
            text=True,
            bufsize=1,  # line-buffered
        )
        process_start_time = time.time()

        # Start a thread to stream stdout to full_recovery.log
        logfile_writer_thread = threading.Thread(target=stream_recovery_output, daemon=True)
        logfile_writer_thread.start()

        return JsonResponse({'success': True})
    except Exception as e:
        print(f"❌ Failed to start recovery: {e}")
        return JsonResponse({'success': False, 'error': str(e)})


def stream_recovery_output():
    """
    Read from the running process stdout and write directly to full_recovery.log line-by-line.
    """
    global current_process, full_recovery_log

    if not current_process or not current_process.stdout:
        return

    try:
        with open(full_recovery_log, 'w', encoding='utf-8') as log_file:
            for line in iter(current_process.stdout.readline, ''):
                if line:
                    log_file.write(line)
                    log_file.flush()
    except Exception as e:
        print(f"❌ Error streaming output: {e}")


def check_recovery_status(request):
    global current_process, last_recovery_result, full_recovery_log

    if current_process:
        poll_status = current_process.poll()
        print(f"[DEBUG] poll() status: {poll_status}")

        if poll_status is None:
            return JsonResponse({'status': 'running'})
        else:
            # Process finished
            try:
                parsed_report = parse_recovery_data()
                last_recovery_result = {
                    'parsed_report': parsed_report
                }
            except Exception as e:
                last_recovery_result = {
                    'error': f'Failed to parse recovery data: {e}',
                    'raw_output': '',
                }

            current_process = None
            return JsonResponse({'status': 'finished'})
    else:
        return JsonResponse({'status': 'finished'})


def stop_recovery(request):
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No active recovery'})


def open_list_file(request, filename):
    file_path = os.path.join(LIST_FOLDER, filename)
    if os.path.exists(file_path):
        os.system(f'notepad "{file_path}"')
        return HttpResponse("OK")
    else:
        return HttpResponse("List file not found.", status=404)


def open_derivation_file(request, filename):
    file_path = os.path.join(DERIVATION_FOLDER, filename)
    if os.path.exists(file_path):
        os.system(f'notepad "{file_path}"')
        return HttpResponse("OK")
    else:
        return HttpResponse("Derivation file not found.", status=404)

def download_recovery_report(request):
    report_path = os.path.join(BASE_DIR, 'full_recovery.log')
    if os.path.exists(report_path):
        with open(report_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename="recovery_report.txt"'
            return response
    else:
        return HttpResponse("Report not found.", status=404)

