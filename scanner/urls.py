from django.urls import path
from scanner.views import (
    seed_repair,
    seed_descramble,
    private_key_repair,
    passphrase_finder,
)
from scanner.views.passphrase_finder import download_passphrase_finder_report_pdf
from scanner.views.seed_repair import (
    download_repair_log,
    open_list_file as open_repair_list_file,
    open_derivation_file as open_repair_derivation_file
)
from scanner.views.seed_descramble import (
    download_recovery_report as download_descramble_report,
    open_list_file as open_descramble_list_file,
    open_derivation_file as open_descramble_derivation_file
)
from scanner.views.reports import download_recovery_report_pdf

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
    path('repair/open-list-file/<str:filename>/', open_repair_list_file, name='open_list_file'),
    path('repair/open-derivation-file/<str:filename>/', open_repair_derivation_file, name='open_derivation_file'),
    path('repair/download/pdf/', download_recovery_report_pdf, {'module_name': 'repair'}, name='download_repair_report_pdf'),

    # ────────────────────────────────────────────────
    # 🔀 Seed Descramble Module
    # ────────────────────────────────────────────────
    path('descramble/', seed_descramble.input_view, name='seed_descramble_input'),
    path('descramble/start-recovery/', seed_descramble.start_recovery, name='seed_descramble_start_recovery'),
    path('descramble/check-recovery-status/', seed_descramble.check_recovery_status, name='seed_descramble_check_status'),
    path('descramble/stop-recovery/', seed_descramble.stop_recovery, name='seed_descramble_stop_recovery'),
    path('descramble/result/', seed_descramble.result_view, name='seed_descramble_result'),
    path('descramble/download-report/', download_descramble_report, name='download_descramble_report'),
    path('descramble/open-list-file/<str:filename>/', open_descramble_list_file, name='descramble_open_list_file'),
    path('descramble/open-derivation-file/<str:filename>/', open_descramble_derivation_file, name='descramble_open_derivation_file'),
    path('descramble/download/pdf/', download_recovery_report_pdf, {'module_name': 'descramble'}, name='download_descramble_report_pdf'),

    # ────────────────────────────────────────────────
    # 🛠️ Private Key Repair Module
    # ────────────────────────────────────────────────
    path('private_key_repair/', private_key_repair.private_key_repair_input, name='private_key_repair_input'),
    path('private_key_repair/start/', private_key_repair.start_private_key_repair, name='start_private_key_repair'),
    path('private_key_repair/check-recovery-status/', private_key_repair.check_private_key_status, name='check_private_key_status'),
    path('private_key_repair/result/', private_key_repair.private_key_repair_result, name='private_key_repair_result'),
    path('private_key_repair/report/', private_key_repair.download_recovery_report, name='download_private_key_repair_report'),
    path('private_key_repair/open-list-file/<str:filename>/', private_key_repair.open_list_file, name='open_pk_list_file'),
    path('private_key_repair/open-addressdb-file/<str:filename>/', private_key_repair.open_addressdb_file, name='open_pk_addressdb_file'),

    # ────────────────────────────────────────────────
    # 🧩 Passphrase Finder Module
    # ────────────────────────────────────────────────
    # Passphrase Finder Module
    path("passphrase_finder/", passphrase_finder.passphrase_finder_input, name="passphrase_finder_input"),
    path("passphrase_finder/start/", passphrase_finder.start_passphrase_finder, name="start_passphrase_finder"),
    path("passphrase_finder/check-recovery-status/", passphrase_finder.check_passphrase_status,
         name="check_passphrase_status"),
    path("passphrase_finder/result/", passphrase_finder.passphrase_finder_result, name="passphrase_finder_result"),
    path("passphrase_finder/open-list-file/<str:filename>/", passphrase_finder.open_list_file,
         name="open_passphrase_list_file"),
    path("passphrase_finder/download/pdf/", passphrase_finder.download_recovery_report,
         name="download_passphrase_finder_report_pdf"),

    # ────────────────────────────────────────────────
    # 🧾 Shared: Dynamic PDF route (for all modules)
    # ────────────────────────────────────────────────
    path('<str:module_name>/download/pdf/', download_recovery_report_pdf, name='download_recovery_report_pdf'),
]
