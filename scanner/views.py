import re
import shlex
import subprocess
import sys
from datetime import datetime
from django.shortcuts import render
from .forms import SeedRecoveryForm

def recover_seed(request):
    if request.method == 'POST':
        form = SeedRecoveryForm(request.POST, request.FILES)
        if form.is_valid():
            python_exec = sys.executable
            constructed_string = form.cleaned_data.get('constructed_string', '').strip()
            raw_seed_phrase = form.cleaned_data.get('seed_phrase', '').strip()  # Optional from structured form

            if not constructed_string:
                return render(request, 'scanner/seed_repair_input.html', {
                    'form': form,
                    'error': 'Command string is required.'
                })

            # Remove accidental inclusion of "python seedrecover.py"
            constructed_string = re.sub(r'^python\s+seedrecover\.py\s*', '', constructed_string)

            try:
                cmd_parts = shlex.split(constructed_string)
                cmd = [python_exec, 'seedrecover.py'] + cmd_parts
            except ValueError as e:
                return render(request, 'scanner/seed_repair_input.html', {
                    'form': form,
                    'error': f"Invalid command string syntax: {e}"
                })

            # Try to extract seed phrase if --mnemonic is used
            faulty_list = []
            if '--mnemonic' in cmd_parts:
                try:
                    idx = cmd_parts.index('--mnemonic')
                    if idx + 1 < len(cmd_parts):
                        parsed_seed = cmd_parts[idx + 1].strip('"')
                        faulty_list = parsed_seed.split()
                except Exception:
                    pass
            elif raw_seed_phrase:
                faulty_list = raw_seed_phrase.split()

            try:
                raw_output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)

                match_line = None
                if "MATCHING SEED FOUND" in raw_output:
                    match_line = "MATCHING SEED FOUND!"
                elif "Seed found:" in raw_output:
                    match_line = "SEED FOUND"

                derivation_match = re.search(r"Matched on Address at derivation path: ([^\n]+)", raw_output)
                seed_found_match = re.search(r"Seed found:\s+([a-z\s]+)", raw_output)
                timestamp_match = re.search(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})", raw_output)
                timestamp = timestamp_match.group(1) if timestamp_match else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                correct_list = seed_found_match.group(1).strip().split() if seed_found_match else []

                context = {
                    'match_line': match_line,
                    'derivation_path': derivation_match.group(1) if derivation_match else "",
                    'timestamp': timestamp,
                    'faulty_seed': " ".join(faulty_list) if faulty_list else "N/A",
                    'correct_seed': " ".join(correct_list),
                    'raw_output': raw_output,
                }

            except subprocess.CalledProcessError as e:
                context = {'error': f"An error occurred:\n{e.output}"}

            return render(request, 'scanner/seed_repair_result.html', context)

        else:
            return render(request, 'scanner/seed_repair_input.html', {'form': form})

    # GET request
    return render(request, 'scanner/seed_repair_input.html', {
        'form': SeedRecoveryForm()
    })

