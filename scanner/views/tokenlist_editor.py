from django.shortcuts import render

def tokenlist_editor(request):
    return render(request, 'scanner/tokenlist_editor.html')
