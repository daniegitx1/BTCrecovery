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

if __name__ == "__main__":
    print("Seedrecover.py started successfully", flush=True)
    print("\nStarting", btcrseed.full_version(), flush=True)

    nogui = '--nogui' in sys.argv or os.environ.get('FORCE_NO_GUI') == '1'
    no_pause = os.environ.get('NO_PAUSE') == '1'

    if not nogui:
        btcrseed.register_autodetecting_wallets()

    mnemonic_sentence, path_coin = btcrseed.main(sys.argv[1:])

    if mnemonic_sentence:
        if not btcrseed.tk_root:
            print("\nSeed found:", mnemonic_sentence, flush=True)

            # ✅ Save recovered seed to output file
            try:
                os.makedirs("runtime", exist_ok=True)
                with open("runtime/recovery_output.txt", "w", encoding="utf-8") as f:
                    f.write(mnemonic_sentence.strip())
            except Exception as e:
                print(f"ERROR: Could not save seed to runtime/recovery_output.txt: {e}", flush=True)

        if btcrseed.tk_root and not nogui:
            btcrseed.show_mnemonic_gui(mnemonic_sentence, path_coin)

        retval = 0

    elif mnemonic_sentence is None:
        retval = 1  # Error occurred
    else:
        retval = 0  # Seed not found, but not an error

    # Wait for any remaining child processes to exit cleanly
    for process in multiprocessing.active_children():
        process.join(1.0)

    # Handle pause
    if not no_pause:
        try:
            if sys.stdin and sys.stdin.isatty():
                input("Press Enter to exit ...")
        except Exception:
            pass

    sys.exit(retval)
