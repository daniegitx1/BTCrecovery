# scanner/forms/seed_repair.py
from django import forms

class SeedRepairForm(forms.Form):
    constructed_string = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Paste or build command string here'}),
        required=False
    )
    wallet_file = forms.FileField(required=False)
    wallet_type = forms.ChoiceField(choices=[
        ('bip39', 'BIP39'),
        ('electrum1', 'Electrum1'),
        ('electrum2', 'Electrum2'),
        # add more if needed
    ])
    master_pub_key = forms.CharField(required=False)
    addresses = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False)
    address_limit = forms.IntegerField(required=False)
    seed_phrase = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
