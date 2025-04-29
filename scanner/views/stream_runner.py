import subprocess
import sys
import shlex
from django.http import JsonResponse
import psutil

# Save global running PID
running_pid = None

def start_recovery(request):
    global running_pid

    args = request.GET.get('args', '')
    if not args:
        return JsonResponse({'error': 'No args provided'}, status=400)

    cmd = f'"{sys.executable}" seedrecover.py {args}'
    print(f"▶️ Starting: {cmd}")

    process = subprocess.Popen(shlex.split(cmd), cwd="C:/Users/danie/PycharmProjects/btcrecover")
    running_pid = process.pid

    return JsonResponse({'success': True, 'pid': running_pid})


def stop_recovery(request):
    global running_pid

    if running_pid is None:
        return JsonResponse({'error': 'No running process'}, status=400)

    try:
        proc = psutil.Process(running_pid)
        proc.terminate()
        running_pid = None
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def check_recovery_status(request):
    global running_pid

    if running_pid is None:
        return JsonResponse({'status': 'idle'})

    try:
        proc = psutil.Process(running_pid)
        if proc.is_running():
            return JsonResponse({'status': 'running'})
    except psutil.NoSuchProcess:
        pass

    running_pid = None
    return JsonResponse({'status': 'finished'})
