from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
import datetime

def download_recovery_report_pdf(request, module_name):
    parsed_report = request.session.get('parsed_report')

    if not parsed_report:
        print("DEBUG: parsed_report is missing from session")
        return HttpResponse("No report data found", status=404)

    template_name = f'pdf_reports/{module_name}_report.html'

    html_string = render_to_string(template_name, {
        'report': parsed_report,
        'generated_on': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    })

    pdf_file = HTML(string=html_string).write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{module_name}_recovery_report.pdf"'
    return response
