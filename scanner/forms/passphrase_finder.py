from django import forms

WALLET_TYPE_CHOICES = [
    ('bip39', 'BIP39'),
    ('', 'Select a wallet type'),
    ('avalanche', 'Avalanche'),
    ('bch', 'Bitcoin Cash'),
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


class PassphraseFinderForm(forms.Form):
    seed_phrase = forms.CharField(
        required=False,
        label="Seed Phrase",
        widget=forms.Textarea(attrs={
            "placeholder": "Enter BIP39 seed words here...",
            "rows": 3,
            "class": "form-control"
        })
    )

    wallet_type = forms.ChoiceField(
        required=False,
        label="Wallet Type",
        choices=WALLET_TYPE_CHOICES,
        widget=forms.Select(attrs={
            "class": "form-control"
        })
    )

    addresses = forms.CharField(
        required=True,
        label="Addresses",
        widget=forms.TextInput(attrs={
            "placeholder": "Enter one or more known addresses",
            "class": "form-control"
        })
    )

    address_limit = forms.IntegerField(
        required=False,
        label="Address Limit",
        initial=10,
        widget=forms.NumberInput(attrs={
            "placeholder": "Max addresses to scan (default 10)",
            "class": "form-control"
        })
    )

    list_file = forms.CharField(
        required=False,
        label="Password List or Token List File",
        widget=forms.TextInput(attrs={
            "placeholder": "Select a file...",
            "class": "form-control",
            "readonly": True
        })
    )
