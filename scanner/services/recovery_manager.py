import os
import subprocess
from django.http import JsonResponse

current_process = None

def start_recovery_process(request):
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

def stop_recovery_process(request):
    global current_process

    if current_process:
        current_process.terminate()
        current_process = None
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'No active recovery'})

def check_recovery_status(request):
    global current_process

    if current_process and current_process.poll() is None:
        return JsonResponse({'status': 'running'})
    else:
        return JsonResponse({'status': 'finished'})
