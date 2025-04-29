from django.shortcuts import render, redirect
from scanner.forms.paperwallet import PaperWalletForm
from scanner.services.paperwallet_runner import run_paperwallet_command

def input_view(request):
    return render(request, 'scanner/paperwallet_input.html', {
        'form': PaperWalletForm()
    })

def result_view(request):
    if request.method != 'POST':
        return redirect('paperwallet_input')

    form = PaperWalletForm(request.POST)
    if not form.is_valid():
        return render(request, 'scanner/paperwallet_input.html', {
            'form': form,
            'error': 'Form validation failed.'
        })

    constructed_string = form.cleaned_data.get('constructed_string', '').strip()
    context = run_paperwallet_command(constructed_string)
    return render(request, 'scanner/paperwallet_result.html', context)
