from django import forms

WALLET_TYPE_CHOICES = [
    ('', 'Select a wallet type'),  # Keep an empty first option
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

class SeedRepairForm(forms.Form):
    constructed_string = forms.CharField(
        label="Seed Recovery Command",
        widget=forms.Textarea(attrs={
            'rows': 4,
            'class': 'form-control',
            'placeholder': 'Paste or build command string here'
        }),
        required=False
    )

    wallet_type = forms.ChoiceField(
        label="Wallet Type",
        choices=WALLET_TYPE_CHOICES,
        initial='bip39',  # ✅ Default
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    addresses = forms.CharField(
        label="Addresses (Optional)",
        widget=forms.Textarea(attrs={
            'rows': 2,
            'class': 'form-control',
            'placeholder': 'Enter known addresses (space or comma separated)'
        }),
        required=False
    )

    address_limit = forms.IntegerField(
        label="Address Limit",
        min_value=1,
        initial=5,  # ✅ Default
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )

    seed_phrase = forms.CharField(
        label="Seed Phrase",
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control full-width',
            'placeholder': 'Enter full or partial seed phrase'
        }),
        required=True
    )

    wordlist_file = forms.CharField(
        label="Wordlist File (Optional)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': './btcrecover/dd-lists/seedwords_plain.txt'
        }),
        required=False
    )

    language = forms.ChoiceField(
        label="Language",
        choices=[
            ('EN', 'English'),
            ('FR', 'French'),
            ('ES', 'Spanish'),
            ('JP', 'Japanese'),
        ],
        initial='EN',  # ✅ Default
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )

    mnemonic_length = forms.IntegerField(
        label="Mnemonic Length",
        initial=24,  # ✅ Default
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 12 or 24'}),
        required=False
    )

