from django.shortcuts import render, redirect
from scanner.forms.password_find import PasswordFindForm
from scanner.services.password_find_runner import run_password_find_command

def input_view(request):
    return render(request, 'scanner/password_find_input.html', {
        'form': PasswordFindForm()
    })

def result_view(request):
    if request.method != 'POST':
        return redirect('password_find_input')

    form = PasswordFindForm(request.POST)
    if not form.is_valid():
        return render(request, 'scanner/password_find_input.html', {
            'form': form,
            'error': 'Form validation failed.'
        })

    constructed_string = form.cleaned_data.get('constructed_string', '').strip()
    context = run_password_find_command(constructed_string)
    return render(request, 'scanner/password_find_result.html', context)
