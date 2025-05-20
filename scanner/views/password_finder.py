import os
from scanner.utilities import parse_password_finder_output
from datetime import datetime
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from weasyprint import HTML
from scanner.forms.password_finder import PasswordFinderForm
from scanner.services import password_finder_runner

PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
LOG_PATH = os.path.join(PROJECT_ROOT, "runtime/descramble_output.log")
REPORT_PATH = os.path.join(PROJECT_ROOT, "runtime/recovery_output.txt")
TIMESTAMP_PATH = os.path.join(PROJECT_ROOT, "runtime/timestamps.txt")


def password_finder_input(request):
    form = PasswordFinderForm()
    return render(request, 'scanner/password_finder_input.html', {'form': form})


def start_password_finder(request):
    args = request.GET.get("args", "")
    if not args:
        return JsonResponse({"success": False, "error": "No args received."})

    try:
        start_time = datetime.now().isoformat()
        with open(TIMESTAMP_PATH, "w") as f:
            f.write(f"Start_Time={start_time}\n")

        password_finder_runner.run(args)
        return JsonResponse({"success": True})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


def stop_password_finder(request):
    password_finder_runner.stop()
    return JsonResponse({"success": True})


def check_recovery_status(request):
    finished = password_finder_runner.check_finished()
    return JsonResponse({"status": "finished" if finished else "running"})


import time

def password_finder_result(request):
    import time

    try:
        with open(TIMESTAMP_PATH, "a") as f:
            f.write(f"End_Time={datetime.now().isoformat()}\n")

        parsed_report = {}
        for _ in range(25):  # Retry for up to 5 seconds
            parsed_report = parse_password_finder_output()
            if parsed_report.get("Recovered_Key") or parsed_report.get("Recovery_Log"):
                break
            time.sleep(0.2)

    except Exception as e:
        return render(request, 'scanner/password_finder_result.html', {'error': str(e)})

    return render(request, 'scanner/password_finder_result.html', {
        'parsed_report': parsed_report
    })


from django.http import FileResponse
from io import BytesIO
from weasyprint import HTML
from datetime import datetime
from scanner.utilities import parse_password_finder_output
from django.template.loader import render_to_string

def download_recovery_report(request):
    parsed_report = parse_password_finder_output()

    html_string = render_to_string("pdf_reports/password_finder_report.html", {
        "report": parsed_report,
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_file)
    pdf_file.seek(0)

    return FileResponse(pdf_file, as_attachment=True, filename="password_finder_report.pdf")
