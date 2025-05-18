import os
import time
import datetime
import subprocess

from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from scanner.forms.seed_repair import SeedRepairForm
from scanner.services import seed_repair_runner
from scanner.utilities import parse_seed_repair_output

from weasyprint import HTML

# ─────────────────────────────────────────────────────
# 📁 Path Configuration
# ─────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
BTRECOVER_DIR = os.path.join(PROJECT_ROOT, "btcrecover")
LIST_FOLDER = os.path.join(BTRECOVER_DIR, "dd-lists")
DERIVATION_FOLDER = os.path.join(PROJECT_ROOT, "derivationpath-lists")
SEEDREPAIR_PATH = os.path.join(PROJECT_ROOT, "seedrecover.py")
LOG_PATH = os.path.join(PROJECT_ROOT, "runtime/seedrepair_output.log")

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
        recovery_log = _read_log_file(LOG_PATH)
        return render(request, 'scanner/seed_repair_result.html', {
            'error': f"Error parsing result: {str(e)}",
            'recovery_log': recovery_log
        })

    if not parsed_report.get("Recovered_Seed"):
        recovery_log = _read_log_file(LOG_PATH)
        return render(request, 'scanner/seed_repair_result.html', {
            'error': 'No matching seeds found.',
            'recovery_log': recovery_log
        })

    request.session['parsed_report'] = parsed_report

    field_list = [
        'Wallet_Type', 'Addresses', 'Address_Limit', 'Language', 'Mnemonic_Length',
        'Wordlist_File', 'Allow_Word_Swaps', 'Disable_Duplicate_Checking', 'Suppress_ETA',
        'Software_Version', 'Start_Time', 'End_Time', 'Full_Command'
    ]

    return render(request, 'scanner/seed_repair_result.html', {
        'parsed_report': parsed_report,
        'field_list': field_list
    })


def _read_log_file(path):
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return "No log file available."


# ─────────────────────────────────────────────────────
# ▶️ Start/Stop/Check Recovery
# ─────────────────────────────────────────────────────

def start_repair(request):
    args = request.GET.get('args', '').strip()
    if not args:
        return JsonResponse({'success': False, 'error': 'No arguments provided.'})

    cmd = seed_repair_runner.build_recovery_command(SEEDREPAIR_PATH, args)
    seed_repair_runner.log_command_to_file(cmd)
    seed_repair_runner.run(cmd)  # ✅ Correct function name
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
    if os.path.exists(LOG_PATH):
        return FileResponse(open(LOG_PATH, 'rb'), as_attachment=True, filename='seedrepair_output.log')
    else:
        return JsonResponse({'error': 'Log file not found.'})


# ─────────────────────────────────────────────────────
# 📂 Open Files (List + Derivation)
# ─────────────────────────────────────────────────────

def open_list_file(request, filename):
    file_path = os.path.join(LIST_FOLDER, filename)
    print("📄 Requested list file:", file_path)

    if not os.path.isfile(file_path):
        return JsonResponse({"success": False, "error": "File not found"})

    try:
        subprocess.Popen(['notepad', file_path])
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})



def open_derivation_file(request, filename):
    file_path = os.path.join(DERIVATION_FOLDER, filename)
    print("📝 Opening derivation file in Notepad:", file_path)

    if os.path.exists(file_path):
        try:
            subprocess.Popen(['notepad', file_path])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)


# ─────────────────────────────────────────────────────
# 🧾 PDF Report Download
# ─────────────────────────────────────────────────────

def download_recovery_report_pdf(request):
    parsed_report = request.session.get('parsed_report')

    if not parsed_report:
        return HttpResponse("No report data found", status=404)

    html_string = render_to_string('pdf_reports/seed_repair_report.html', {
        'report': parsed_report,
        'generated_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recovery_report.pdf"'
    return response
