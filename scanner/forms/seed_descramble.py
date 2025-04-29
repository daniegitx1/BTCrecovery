from django import forms

class SeedDescrambleForm(forms.Form):
    tokenlist_file = forms.FileField(required=False)

    wallet_type = forms.ChoiceField(
        choices=[
            ('bip39', 'BIP39'),
            ('electrum1', 'Electrum v1'),
            ('electrum2', 'Electrum v2+'),
            ('bip38', 'BIP38 Encrypted Key'),
            ('tron', 'Tron Wallet'),
        ],
        initial='bip39',
        required=True
    )

    addresses = forms.CharField(required=False)
    address_limit = forms.IntegerField(initial=5, required=False)
    mnemonic_length = forms.IntegerField(initial=12, required=False)

    # ✅ Language without Auto-Detect
    language = forms.ChoiceField(
        choices=[
            ('EN', 'English'),
            ('ES', 'Spanish'),
            ('FR', 'French'),
            ('IT', 'Italian'),
            ('JA', 'Japanese'),
            ('ZH', 'Chinese'),
        ],
        initial='EN',
        required=False
    )

    dsw = forms.BooleanField(required=False, initial=True)
    noeta = forms.BooleanField(required=False, initial=True)
    nodup = forms.BooleanField(required=False, initial=True)
