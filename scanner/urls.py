# scanner/urls.py

from django.urls import path
# Main views
from scanner import views
# Task-specific modules
from scanner.views import seed_repair, seed_descramble
# Shared downloads and utilities
from scanner.views.seed_repair import (
    download_repair_log,
    open_list_file,
    open_derivation_file
)
from scanner.views.seed_descramble import download_recovery_report




urlpatterns = [
    # ────────────────────────────────────────────────
    # 📋 Dashboard
    # ────────────────────────────────────────────────
    path('', seed_repair.dashboard, name='dashboard'),

    # ────────────────────────────────────────────────
    # 🔧 Seed Repair Module
    # ────────────────────────────────────────────────
    path('repair/', seed_repair.seed_repair_input, name='seed_repair_input'),
    path('repair/start-recovery/', seed_repair.start_repair, name='start_seed_repair'),
    path('repair/check-recovery-status/', seed_repair.check_repair_status, name='check_seed_repair_status'),
    path('repair/stop-recovery/', seed_repair.stop_repair, name='stop_seed_repair'),
    path('repair/result/', seed_repair.seed_repair_result, name='seed_repair_result'),
    path('repair/download-log/', download_repair_log, name='download_repair_log'),
    path('repair/open-list-file/<str:filename>/', seed_repair.open_list_file, name='repair_open_list_file'),

    # ────────────────────────────────────────────────
    # 🔀 Seed Descramble Module
    # ────────────────────────────────────────────────
    path('descramble/', seed_descramble.input_view, name='seed_descramble_input'),
    path('descramble/start-recovery/', seed_descramble.start_recovery, name='seed_descramble_start_recovery'),
    path('descramble/check-recovery-status/', seed_descramble.check_recovery_status, name='seed_descramble_check_status'),
    path('descramble/stop-recovery/', seed_descramble.stop_recovery, name='seed_descramble_stop_recovery'),
    path('descramble/result/', seed_descramble.result_view, name='seed_descramble_result'),
    path('descramble/download-report/', download_recovery_report, name='download_recovery_report'),
    path('open-list-file/<str:filename>/', seed_descramble.open_list_file, name='open_list_file'),
    path('open-derivation-file/<str:filename>/', seed_descramble.open_derivation_file, name='open_derivation_file'),

    path("repair/open-list-file/<str:filename>/", open_list_file, name="open_list_file"),
    path("repair/open-derivation-file/<str:filename>/", open_derivation_file, name="open_derivation_file"),

]
