from btcrecover import btcrseed
import multiprocessing

def run_btcrseed(arguments):
    btcrseed.register_autodetecting_wallets()
    mnemonic_sentence, path_coin = btcrseed.main(arguments)

    # Clean up child processes
    for process in multiprocessing.active_children():
        process.join(1.0)

    return mnemonic_sentence, path_coin
