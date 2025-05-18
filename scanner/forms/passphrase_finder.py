from django import forms

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
        choices=[
            ('', 'BIP39 (default)'),
            ('electrum2', 'Electrum 2'),
            ('ethereum', 'Ethereum'),
            ('ethereumvalidator', 'Ethereum Validator'),
            ('bch', 'Bitcoin Cash'),
            ('dash', 'Dash'),
        ],
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
