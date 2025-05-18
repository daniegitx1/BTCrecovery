import os
import time
import subprocess
from io import BytesIO
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from scanner.services import passphrase_finder_runner
from scanner.utilities import parse_passphrase_output, parse_recovery_output  # you'll add this
from scanner.forms.passphrase_finder import PassphraseFinderForm  # optional

# ─────────────────────────────────────────────────────
# 📁 Paths
# ─────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
TOKENLIST_DIR = os.path.join(PROJECT_ROOT, "btcrecover", "dd-lists")

# ─────────────────────────────────────────────────────
# 🌐 Views
# ─────────────────────────────────────────────────────

from scanner.forms.passphrase_finder import PassphraseFinderForm

def passphrase_finder_input(request):
    form = PassphraseFinderForm()
    return render(request, "scanner/passphrase_finder_input.html", {"form": form})


def start_passphrase_finder(request):
    args = request.GET.get("args", "").strip()
    if not args:
        return JsonResponse({"success": False, "error": "No arguments provided"})
    try:
        cmd = passphrase_finder_runner.build_recovery_command(
            os.path.join(PROJECT_ROOT, "btcrecover.py"), args
        )
        passphrase_finder_runner.log_command_to_file(cmd)
        passphrase_finder_runner.run(cmd)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})

def check_passphrase_status(request):
    parsed = parse_passphrase_output()
    if parsed.get("Recovered_Key"):
        return JsonResponse({"status": "finished"})
    return JsonResponse({"status": "running"})

def passphrase_finder_result(request):
    parsed_report = {}

    try:
        for _ in range(20):
            parsed_report = parse_passphrase_output()
            if parsed_report.get("Recovered_Key"):
                break
            time.sleep(0.2)
    except Exception as e:
        return render(request, "scanner/passphrase_finder_result.html", {
            "error": f"Error parsing result: {str(e)}"
        })

    if not parsed_report.get("Recovered_Key"):
        return render(request, "scanner/passphrase_finder_result.html", {
            "error": "No valid key recovered.",
            "recovery_log": parsed_report.get("Recovery_Log", "")
        })

    field_list = [
        "Wallet_Type", "Address", "Passwordlist_File", "Tokenlist_File",
        "Software_Version", "Start_Time", "End_Time", "Full_Command"
    ]

    return render(request, "scanner/passphrase_finder_result.html", {
        "parsed_report": parsed_report,
        "field_list": field_list
    })

def download_recovery_report(request):
    parsed_report = parse_passphrase_output()

    html_string = render_to_string("pdf_reports/passphrase_finder_report.html", {
        "report": parsed_report,
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    })

    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_file)
    pdf_file.seek(0)

    return FileResponse(
        pdf_file,
        as_attachment=True,
        filename="passphrase_recovery_report.pdf",
        content_type='application/pdf'
    )

def open_list_file(request, filename):
    filepath = os.path.join(TOKENLIST_DIR, filename)
    try:
        subprocess.Popen(["notepad.exe", filepath])
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

from weasyprint import HTML
from io import BytesIO
from django.template.loader import render_to_string

def download_passphrase_finder_report_pdf(request):
    parsed_report = parse_recovery_output()
    html_string = render_to_string("pdf_reports/passphrase_finder_report.html", {
        "report": parsed_report,
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_file)
    pdf_file.seek(0)
    return FileResponse(pdf_file, as_attachment=True, filename="passphrase_finder_report.pdf")

