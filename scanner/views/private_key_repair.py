from django.shortcuts import render, redirect
from scanner.forms.private_key_repair import PrivateKeyRepairForm
from scanner.services.private_key_repair_runner import run_private_key_repair_command

def input_view(request):
    return render(request, 'scanner/private_key_repair_input.html', {
        'form': PrivateKeyRepairForm()
    })

def result_view(request):
    if request.method != 'POST':
        return redirect('private_key_repair_input')

    form = PrivateKeyRepairForm(request.POST)
    if not form.is_valid():
        return render(request, 'scanner/private_key_repair_input.html', {
            'form': form,
            'error': 'Form validation failed.'
        })

    constructed_string = form.cleaned_data.get('constructed_string', '').strip()
    context = run_private_key_repair_command(constructed_string)
    return render(request, 'scanner/private_key_repair_result.html', context)
