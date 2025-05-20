from django import forms

class PasswordFinderForm(forms.Form):
    wallet = forms.FileField(
        required=True,
        label="Wallet File or Folder",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    MODE_CHOICES = [
        ('tokenlist', 'Use Tokenlist'),
        ('passwordlist', 'Use Passwordlist'),
    ]
    mode = forms.ChoiceField(
        required=True,
        label="Password Input Mode",
        choices=MODE_CHOICES,
        widget=forms.RadioSelect
    )

    tokenlist = forms.FileField(
        required=False,
        label="Tokenlist File",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    passwordlist = forms.FileField(
        required=False,
        label="Passwordlist File",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    WALLET_TYPE_CHOICES = [
        ('', 'Select a wallet type'),
        ('bip39', 'BIP39'),
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

    wallet_type = forms.ChoiceField(
        required=False,
        label="Wallet Type (--wallet-type)",
        choices=WALLET_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select mb-3'})
    )

    typos = forms.IntegerField(
        required=False,
        label="Max Typos (--typos)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    typos_capslock = forms.BooleanField(required=False, label="Caps Lock (--typos-capslock)")
    typos_swap = forms.BooleanField(required=False, label="Swap Adjacent (--typos-swap)")
    typos_repeat = forms.BooleanField(required=False, label="Repeat Character (--typos-repeat)")
    typos_delete = forms.BooleanField(required=False, label="Delete Character (--typos-delete)")
    typos_case = forms.BooleanField(required=False, label="Case Change (--typos-case)")

    typos_replace = forms.CharField(
        required=False,
        label="Replace Char (--typos-replace x)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    typos_insert = forms.CharField(
        required=False,
        label="Insert Char (--typos-insert x)",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    typos_map = forms.FileField(
        required=False,
        label="Typo Map (--typos-map file.txt)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    autosave = forms.FileField(
        required=False,
        label="Autosave (--autosave file.txt)",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    skip = forms.IntegerField(
        required=False,
        label="Skip (--skip n)",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
