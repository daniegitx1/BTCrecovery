import os
import time
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from scanner.forms.seed_repair import SeedRepairForm
from scanner.services import seed_repair_runner
from scanner.utilities import parse_seed_repair_output

# ─────────────────────────────────────────────────────
# 📁 Path Configuration
# ─────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
BTRECOVER_DIR = os.path.join(PROJECT_ROOT, "btcrecover")

SEEDREPAIR_PATH = os.path.join(PROJECT_ROOT, "seedrecover.py")
LOG_PATH = os.path.join(PROJECT_ROOT, "runtime/seedrepair_output.log")

LIST_FOLDER = os.path.join(BTRECOVER_DIR, "dd-lists")
DERIVATION_FOLDER = os.path.join(PROJECT_ROOT, "derivationpath-lists")



# ─────────────────────────────────────────────────────
# 🚀 Seed Repair Views
# ─────────────────────────────────────────────────────

def dashboard(request):
    return render(request, 'scanner/dashboard.html')

def seed_repair_input(request):
    return render(request, 'scanner/seed_repair_input.html', {
        'form': SeedRepairForm()
    })

def seed_repair_result(request):
    parsed_report = {}

    try:
        for _ in range(10):
            parsed_report = parse_seed_repair_output()
            if parsed_report.get("Recovered_Seed"):
                break
            time.sleep(0.2)
    except Exception as e:
        return render(request, 'scanner/seed_repair_result.html', {'error': f"Error parsing result: {str(e)}"})

    if not parsed_report.get("Recovered_Seed"):
        return render(request, 'scanner/seed_repair_result.html', {'error': 'No matching seeds found.'})

    field_list = [
        'Wallet_Type', 'Addresses', 'Address_Limit', 'Language', 'Mnemonic_Length',
        'Wordlist_File', 'Allow_Word_Swaps', 'Disable_Duplicate_Checking', 'Suppress_ETA',
        'Software_Version', 'Start_Time', 'End_Time', 'Full_Command'
    ]

    return render(request, 'scanner/seed_repair_result.html', {
        'parsed_report': parsed_report,
        'field_list': field_list
    })

def start_repair(request):
    args = request.GET.get('args', '').strip()
    if not args:
        return JsonResponse({'success': False, 'error': 'No arguments provided.'})

    cmd = seed_repair_runner.build_recovery_command(SEEDREPAIR_PATH, args)
    seed_repair_runner.log_command_to_file(cmd)
    seed_repair_runner.run_repair_command(cmd)
    return JsonResponse({'success': True})

def stop_repair(request):
    success = seed_repair_runner.stop_repair_command()
    return JsonResponse({'success': success})

def check_repair_status(request):
    is_running = seed_repair_runner.ACTIVE_PROCESS is not None
    return JsonResponse({'status': 'running' if is_running else 'finished'})

# ─────────────────────────────────────────────────────
# 📄 Log Download
# ─────────────────────────────────────────────────────

def download_repair_log(request):
    file_path = os.path.join(PROJECT_ROOT, "runtime", "seedrepair_output.log")
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='seedrepair_output.log')
    else:
        return JsonResponse({'error': 'Log file not found.'})

# ─────────────────────────────────────────────────────
# 📂 Open List File
# ─────────────────────────────────────────────────────

from django.http import JsonResponse
import os

def open_list_file(request, filename):
    file_path = os.path.join(LIST_FOLDER, filename)
    print("🔍 Trying to open:", file_path)

    if os.path.exists(file_path):
        print("✅ File exists.")
        print("✅ Readable:", os.access(file_path, os.R_OK))
        os.startfile(file_path)
        return JsonResponse({'success': True})
    else:
        print("❌ File not found at:", file_path)  # <== Add this
        return JsonResponse({'error': 'File not found.'}, status=404)




def open_derivation_file(request, filename):
    file_path = os.path.join(DERIVATION_FOLDER, filename)
    print("🔍 Trying to open:", file_path)

    if os.path.exists(file_path):
        try:
            os.startfile(file_path)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)

