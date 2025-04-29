import sys
import os
import multiprocessing
import sys

# 🚀 Block all tkinter imports system-wide if --nogui or FORCE_NO_GUI
if '--nogui' in sys.argv or os.environ.get('FORCE_NO_GUI') == '1':
    sys.modules['tkinter'] = None
    sys.modules['tkinter.messagebox'] = None
    sys.modules['tkinter.simpledialog'] = None

from btcrecover import btcrseed

# ✅ Only print once in the real main process
if __name__ == "__main__":
    print("Seedrecover.py started successfully")
    sys.stdout.flush()

nogui = '--nogui' in sys.argv or os.environ.get('FORCE_NO_GUI') == '1'
no_pause = ('NO_PAUSE' in os.environ and os.environ['NO_PAUSE'] == '1')  # ✅ Correct detection

if __name__ == "__main__":
    print('', flush=True)
    print("Starting", btcrseed.full_version(), flush=True)

    if not nogui:
        btcrseed.register_autodetecting_wallets()

    mnemonic_sentence, path_coin = btcrseed.main(sys.argv[1:])

    if mnemonic_sentence:
        if not btcrseed.tk_root:
            print('', flush=True)
            print("Seed found:", mnemonic_sentence, flush=True)
            # Save recovered seed to file
            try:
                with open("recovery_output.txt", "w", encoding="utf-8") as f:
                    f.write(mnemonic_sentence.strip())
            except Exception as e:
                print(f"Failed to save seed to file: {e}", flush=True)

        if btcrseed.tk_root and not nogui:
            btcrseed.show_mnemonic_gui(mnemonic_sentence, path_coin)

        retval = 0

    elif mnemonic_sentence is None:
        retval = 1  # Error occurred

    else:
        retval = 0  # Seed not found already printed

    # Wait for any remaining child processes to exit cleanly
    for process in multiprocessing.active_children():
        process.join(1.0)

    # 🚀 FINAL no_pause logic (fixed)
    if no_pause:
        # 🚀 Skip pause completely
        pass
    else:
        try:
            if sys.stdin and sys.stdin.isatty():
                input("Press Enter to exit ...")
        except Exception:
            pass
    # After seed found and just before sys.exit(retval):

    # New final safeguard to always write the seed if found
    if mnemonic_sentence:
        try:
            with open("recovery_output.txt", "w", encoding="utf-8") as f:
                f.write(mnemonic_sentence.strip())
        except Exception as e:
            print(f"ERROR: Could not save seed to recovery_output.txt: {e}", flush=True)

    sys.exit(retval)
