from django.shortcuts import render, redirect
from scanner.forms.passphrase_find import PassphraseFindForm
from scanner.services.passphrase_find_runner import run_passphrase_find_command

def input_view(request):
    return render(request, 'scanner/passphrase_find_input.html', {
        'form': PassphraseFindForm()
    })

def result_view(request):
    if request.method != 'POST':
        return redirect('passphrase_find_input')

    form = PassphraseFindForm(request.POST)
    if not form.is_valid():
        return render(request, 'scanner/passphrase_find_input.html', {
            'form': form,
            'error': 'Form validation failed.'
        })

    constructed_string = form.cleaned_data.get('constructed_string', '').strip()
    context = run_passphrase_find_command(constructed_string)
    return render(request, 'scanner/passphrase_find_result.html', context)
