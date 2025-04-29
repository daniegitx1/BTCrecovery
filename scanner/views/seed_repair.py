# scanner/views/seed_repair.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
import os
import subprocess
import sys

from scanner.forms.seed_repair import SeedRepairForm
from scanner.services.seed_repair_runner import run_seed_repair_command

# ✅ Globals
current_process = None  # Track running recovery
last_recovery_result = None  # Save last finished recovery result

def dashboard(request):
    return render(request, 'scanner/dashboard.html')

def input_view(request):
    return render(request, 'scanner/seed_repair_input.html', {
        'form': SeedRepairForm()
    })

def result_view(request):
    global last_recovery_result

    if request.method == 'POST':
        constructed_string = request.POST.get('constructed_string', '').strip()
        raw_seed_phrase = request.POST.get('seed_phrase', '').strip()

        if not constructed_string:
            return redirect('seed_repair_input')

        context = run_seed_repair_command(constructed_string, raw_seed_phrase)
        last_recovery_result = context
        return render(request, 'scanner/seed_repair_result.html', context)

    elif last_recovery_result:
        context = last_recovery_result
        last_recovery_result = None  # Clear after showing once
        return render(request, 'scanner/seed_repair_result.html', context)

    else:
        return redirect('seed_repair_input')

def start_recovery(request):
    global current_process
    args = request.GET.get('args', '')

    cmd = [os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe"), "seedrecover.py"] + args.split()

    try:
        current_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=os.getcwd()
        )
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def stop_recovery(request):
    global current_process
    if current_process:
        current_process.terminate()
        current_process = None
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No active recovery'})

def check_recovery_status(request):
    global current_process, last_recovery_result

    if current_process and current_process.poll() is None:
        return JsonResponse({'status': 'running'})

    elif current_process and current_process.poll() is not None:
        try:
            output, _ = current_process.communicate(timeout=5)
            output = output.decode('utf-8') if isinstance(output, bytes) else output
            constructed_string = request.GET.get('args', '')
            raw_seed_phrase = request.GET.get('seed_phrase', '')

            # ✅ Use parsing only, don't re-run recovery
            last_recovery_result = run_seed_repair_command(constructed_string, raw_seed_phrase)

        except Exception:
            last_recovery_result = None

        current_process = None
        return JsonResponse({'status': 'finished'})

    else:
        return JsonResponse({'status': 'finished'})
