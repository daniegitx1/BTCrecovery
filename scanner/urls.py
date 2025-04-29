# scanner/urls.py

from django.urls import path
from scanner.views import seed_repair, seed_descramble  # ✅ Correct import
from scanner.views.seed_descramble import download_recovery_report

urlpatterns = [
    # Dashboard
    path('', seed_repair.dashboard, name='dashboard'),

    # Seed Repair
    path('repair/', seed_repair.input_view, name='seed_repair_input'),
    path('repair/result/', seed_repair.result_view, name='seed_repair_result'),
    path('repair/start-recovery/', seed_repair.start_recovery, name='seed_repair_start_recovery'),
    path('repair/stop-recovery/', seed_repair.stop_recovery, name='seed_repair_stop_recovery'),
    path('repair/check-recovery-status/', seed_repair.check_recovery_status, name='seed_repair_check_status'),

    # Seed Descramble
    path('descramble/', seed_descramble.input_view, name='seed_descramble_input'),
    path('descramble/result/', seed_descramble.result_view, name='seed_descramble_result'),
    path('descramble/start-recovery/', seed_descramble.start_recovery, name='seed_descramble_start_recovery'),
    path('descramble/stop-recovery/', seed_descramble.stop_recovery, name='seed_descramble_stop_recovery'),
    path('descramble/check-recovery-status/', seed_descramble.check_recovery_status, name='seed_descramble_check_status'),

    # File openers
    path('open-list-file/<str:filename>/', seed_descramble.open_list_file, name='open_list_file'),
    path('open-derivation-file/<str:filename>/', seed_descramble.open_derivation_file, name='open_derivation_file'),

    path('descramble/download-report/', download_recovery_report, name='download_recovery_report'),

]

