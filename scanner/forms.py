from django import forms

WALLET_TYPE_CHOICES = [
    ('avalanche', 'Avalanche'),
    ('bch', 'Bitcoin Cash'),
    ('bip39', 'BIP39'),
    ('bitcoinj', 'BitcoinJ'),
    ('blockchainpasswordv2', 'Blockchain Password v2'),
    ('blockchainpasswordv3', 'Blockchain Password v3'),
    ('cardano', 'Cardano'),
    ('cosmos', 'Cosmos'),
    ('dash', 'Dash'),
    ('digibyte', 'DigiByte'),
    ('dogecoin', 'Dogecoin'),
    ('electrum1', 'Electrum 1.x'),
    ('electrum2', 'Electrum 2.x'),
    ('ethereum', 'Ethereum'),
    ('ethereumvalidator', 'Ethereum Validator'),
    ('groestlecoin', 'Groestlecoin'),
    ('helium', 'Helium'),
    ('litecoin', 'Litecoin'),
    ('monacoin', 'Monacoin'),
    ('multiversx', 'MultiversX'),
    ('polkadotsubstrate', 'Polkadot/Substrate'),
    ('ripple', 'Ripple'),
    ('secretnetworknew', 'Secret Network (new)'),
    ('secretnetworkold', 'Secret Network (old)'),
    ('solana', 'Solana'),
    ('stacks', 'Stacks'),
    ('stellar', 'Stellar'),
    ('tezos', 'Tezos'),
    ('tron', 'Tron'),
    ('vertcoin', 'Vertcoin'),
    ('zilliqa', 'Zilliqa'),
]

class SeedRecoveryForm(forms.Form):
    wallet_file = forms.FileField(required=False, label="Wallet File (Optional)")
    wallet_type = forms.ChoiceField(choices=WALLET_TYPE_CHOICES, required=False, label="Wallet Type")
    master_pub_key = forms.CharField(required=False, label="Master Public Key (xpub/ypub/zpub)")
    addresses = forms.CharField(required=False, label="Addresses (space or comma-separated)")
    address_limit = forms.IntegerField(initial=10, min_value=1, required=False, label="Address Limit")
    seed_phrase = forms.CharField(widget=forms.Textarea, required=False, label="Seed Phrase")
    constructed_string = forms.CharField(widget=forms.Textarea, required=True, label="Command-line String")
