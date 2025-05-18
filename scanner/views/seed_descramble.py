import os
import time
import datetime
import subprocess

from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from scanner.forms.seed_descramble import SeedDescrambleForm
from scanner.services import seed_descramble_runner
from scanner.utilities import parse_descramble_output

from weasyprint import HTML

# ──────────────────────────────────────────────────────────
# 📁 Path Configuration
# ───────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
BTRECOVER_DIR = os.path.join(PROJECT_ROOT, "btcrecover")
LIST_FOLDER = os.path.join(BTRECOVER_DIR, "dd-lists")
DERIVATION_FOLDER = os.path.join(PROJECT_ROOT, "derivationpath-lists")
DESCRAMBLE_PATH = os.path.join(PROJECT_ROOT, "seedrecover.py")
LOG_PATH = os.path.join(PROJECT_ROOT, "runtime/seeddescramble_output.log")

# ───────────────────────────────────────────────────────
# 🚀 Seed Descramble Views
# ───────────────────────────────────────────────────────

def input_view(request):
    return render(request, 'scanner/seed_descramble_input.html', {
        'form': SeedDescrambleForm()
    })

def result_view(request):
    parsed_report = {}

    try:
        for _ in range(10):
            parsed_report = parse_descramble_output()
            if parsed_report.get("Recovered_Seed"):
                break
            time.sleep(0.2)
    except Exception as e:
        recovery_log = _read_log_file(LOG_PATH)
        return render(request, 'scanner/seed_descramble_result.html', {
            'error': f"Error parsing result: {str(e)}",
            'recovery_log': recovery_log
        })

    if not parsed_report.get("Recovered_Seed"):
        recovery_log = _read_log_file(LOG_PATH)
        return render(request, 'scanner/seed_descramble_result.html', {
            'error': 'No valid descrambled seed found.',
            'recovery_log': recovery_log
        })

    request.session['parsed_report'] = parsed_report

    field_list = [
        'Wallet_Type', 'Addresses', 'Address_Limit', 'Language', 'Mnemonic_Length',
        'Wordlist_File', 'Disable_Duplicate_Checking', 'Suppress_ETA',
        'Software_Version', 'Start_Time', 'End_Time', 'Full_Command'
    ]

    return render(request, 'scanner/seed_descramble_result.html', {
        'parsed_report': parsed_report,
        'field_list': field_list
    })

def _read_log_file(path):
    if os.path.exists(path):
        with open(path, encoding='utf-8') as f:
            return f.read()
    return "No log file available."

# ▶️ Start/Stop/Check Recovery

def start_recovery(request):
    args = request.GET.get('args', '').strip()
    if not args:
        return JsonResponse({'success': False, 'error': 'No arguments provided.'})

    cmd = seed_descramble_runner.build_recovery_command(DESCRAMBLE_PATH, args)
    seed_descramble_runner.log_command_to_file(cmd)
    seed_descramble_runner.run(cmd)
    return JsonResponse({'success': True})

def stop_recovery(request):
    success = seed_descramble_runner.stop_recovery_command()
    return JsonResponse({'success': success})

def check_recovery_status(request):
    is_running = seed_descramble_runner.ACTIVE_PROCESS is not None
    return JsonResponse({'status': 'running' if is_running else 'finished'})

# 📂 Open Files in Notepad

def open_list_file(request, filename):
    file_path = os.path.join(LIST_FOLDER, filename)
    print("📝 Opening list file in Notepad:", file_path)

    if os.path.exists(file_path):
        try:
            subprocess.Popen(['notepad', file_path])
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)

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

# 📟 PDF Report Download

def download_recovery_report(request):
    parsed_report = request.session.get('parsed_report')

    if not parsed_report:
        return HttpResponse("No report data found", status=404)

    html_string = render_to_string('pdf_reports/seed_descramble_report.html', {
        'report': parsed_report,
        'generated_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="descramble_report.pdf"'
    return response
