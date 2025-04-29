import subprocess
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt  # ✅ Add this
from django.conf import settings
import os

@csrf_exempt
def open_tokenlist_file(request):
    try:
        from django.conf import settings
        print("🔍 open_tokenlist_file view REACHED")

        filename = request.POST.get('filename')
        if not filename:
            return JsonResponse({'error': 'No file specified.'}, status=400)

        search_root = os.path.join(settings.BASE_DIR, "btcrecover", "media", "tokenlists")

        print(f"🔍 Searching for: {filename} in {search_root}")

        match_path = None
        for root, _, files in os.walk(search_root):
            print(f"📁 Checking: {root}")
            for file in files:
                print(f"— {file}")
            if filename in files:
                match_path = os.path.join(root, filename)
                print(f"✅ Match found: {match_path}")
                break

        if not match_path or not os.path.exists(match_path):
            return JsonResponse({'error': 'File not found.'}, status=404)

        subprocess.Popen(["start", "", match_path], shell=True)
        return JsonResponse({'success': True})

    except Exception as e:
        print("❌ Exception:", str(e))
        return JsonResponse({'error': str(e)}, status=500)

    # ✅ Safety fallback: return something even if nothing else hit
    return JsonResponse({'error': 'Unreachable code was reached.'}, status=500)
