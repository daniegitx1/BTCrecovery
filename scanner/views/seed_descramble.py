# scanner/views/seed_descramble.py

import os
from django.http import JsonResponse, FileResponse
from django.shortcuts import render
from scanner.forms.seed_descramble import SeedDescrambleForm
from scanner.services import seed_descramble_runner
from scanner.utilities import parse_descramble_output

# ─────────────────────────────────────────────────────
# 🔧 Project Configuration
# ─────────────────────────────────────────────────────

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
SEEDRECOVER_PATH = os.path.join(PROJECT_ROOT, "seedrecover.py")
LOG_PATH = os.path.join(PROJECT_ROOT, "runtime/descramble_output.log")

# ─────────────────────────────────────────────────────
# 🌱 Input Page
# ─────────────────────────────────────────────────────

def input_view(request):
    return render(request, 'scanner/seed_descramble_input.html', {
        'form': SeedDescrambleForm()
    })

# ─────────────────────────────────────────────────────
# 🚀 Recovery Execution
# ─────────────────────────────────────────────────────

def start_recovery(request):
    args = request.GET.get('args', '').strip()
    if not args:
        return JsonResponse({'success': False, 'error': 'No arguments provided.'})

    cmd = seed_descramble_runner.build_recovery_command(SEEDRECOVER_PATH, args)
    seed_descramble_runner.log_command_to_file(cmd)
    seed_descramble_runner.run_seed_descramble_command(cmd)
    return JsonResponse({'success': True})

def stop_recovery(request):
    success = seed_descramble_runner.stop_seed_descramble_command()
    return JsonResponse({'success': success})

def check_recovery_status(request):
    is_running = seed_descramble_runner.ACTIVE_PROCESS is not None
    return JsonResponse({'status': 'running' if is_running else 'finished'})

# ─────────────────────────────────────────────────────
# 📄 Result Page
# ─────────────────────────────────────────────────────

def result_view(request):
    try:
        parsed_report = parse_descramble_output()
    except Exception as e:
        return render(request, 'scanner/seed_descramble_result.html', {
            'error': f"Error parsing result: {str(e)}"
        })

    if not parsed_report or not parsed_report.get("Recovered Seed"):
        return render(request, 'scanner/seed_descramble_result.html', {
            'error': "No matching seeds found."
        })

    return render(request, 'scanner/seed_descramble_result.html', {
        'parsed_report': parsed_report
    })

# ─────────────────────────────────────────────────────
# 📥 Log Download
# ─────────────────────────────────────────────────────

def download_recovery_report(request):
    file_path = os.path.join(PROJECT_ROOT, "runtime", "descramble_output.log")
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename='descramble_output.log')
    else:
        return JsonResponse({'error': 'Log file not found.'}, status=404)

# ─────────────────────────────────────────────────────
# 📂 Token / Path Preview
# ─────────────────────────────────────────────────────

def open_list_file(request, filename):
    file_path = os.path.join(PROJECT_ROOT, "btcrecover", "dd-lists", filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)

def open_derivation_file(request, filename):
    file_path = os.path.join(PROJECT_ROOT, "derivationpath-lists", filename)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), content_type='text/plain')
    else:
        return JsonResponse({'error': 'File not found.'}, status=404)
