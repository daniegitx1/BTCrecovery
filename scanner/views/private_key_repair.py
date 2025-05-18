import os
import time
import subprocess
from django.shortcuts import render
from django.http import JsonResponse, FileResponse, HttpResponse
from scanner.services import private_key_repair_runner
from scanner.utilities import parse_recovery_output  # shared parser
from weasyprint import HTML

# ─────────────────────────────────────────────────────
# 🔧 Paths
# ─────────────────────────────────────────────────────
PROJECT_ROOT = os.path.abspath("C:/Users/danie/PycharmProjects/btcrecover")
RUNTIME_DIR = os.path.join(PROJECT_ROOT, "runtime")
LOG_PATH = os.path.join(RUNTIME_DIR, "descramble_output.log")
TOKENLIST_DIR = os.path.join(PROJECT_ROOT, "btcrecover", "dd-lists")

# ─────────────────────────────────────────────────────
# 🌐 Views
# ─────────────────────────────────────────────────────

def private_key_repair_input(request):
    return render(request, "scanner/private_key_repair_input.html")


def start_private_key_repair(request):
    if request.method == "POST":
        command = request.POST.get("command", "")
        success = private_key_repair_runner.run(command)
        return JsonResponse({"status": "started" if success else "error"})
    return JsonResponse({"status": "invalid"})


def private_key_repair_result(request):
    print("🧠 result view CALLED")  # Debug log
    parsed_report = {}

    try:
        # Wait up to ~4 seconds for the recovered key to appear
        for _ in range(20):
            parsed_report = parse_recovery_output()
            if parsed_report.get("Recovered_Key"):  # Wait for actual result
                print("✅ Parsed recovered key:", parsed_report["Recovered_Key"])
                break
            time.sleep(0.2)

    except Exception as e:
        return render(request, "scanner/private_key_repair_result.html", {
            "error": f"Error parsing result: {str(e)}"
        })

    if not parsed_report.get("Recovered_Key"):
        return render(request, "scanner/private_key_repair_result.html", {
            "error": "No valid private key recovered.",
            "recovery_log": parsed_report.get("Recovery_Log", "")
        })

    field_list = [
        "Wallet_Type", "Address", "Tokenlist_File",
        "Software_Version", "Start_Time", "End_Time", "Full_Command"
    ]

    return render(request, "scanner/private_key_repair_result.html", {
        "parsed_report": parsed_report,
        "field_list": field_list
    })


from io import BytesIO

def download_recovery_report(request):
    parsed_report = parse_recovery_output()

    html_string = render(request, "pdf_reports/private_key_repair_report.html", {
        "report": parsed_report,
        "generated_on": time.strftime("%Y-%m-%d %H:%M:%S")
    }).content.decode("utf-8")

    # Generate PDF in memory
    pdf_file = BytesIO()
    HTML(string=html_string).write_pdf(target=pdf_file)
    pdf_file.seek(0)

    return FileResponse(
        pdf_file,
        as_attachment=True,
        filename="private_key_recovery_report.pdf",
        content_type='application/pdf'
    )


from scanner.utilities import parse_recovery_output

def check_private_key_status(request):
    parsed = parse_recovery_output()
    if parsed.get("Recovered_Key"):
        return JsonResponse({"status": "finished"})
    return JsonResponse({"status": "running"})


def open_list_file(request, filename):
    filepath = os.path.join(TOKENLIST_DIR, filename)
    try:
        subprocess.Popen(["notepad.exe", filepath])
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


def open_addressdb_file(request, filename):
    filepath = os.path.join(TOKENLIST_DIR, filename)
    try:
        subprocess.Popen(["notepad.exe", filepath])
        return HttpResponse("OK")
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)
