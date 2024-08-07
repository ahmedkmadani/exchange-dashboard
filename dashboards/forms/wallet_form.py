from django import forms
from ..models import Wallet


class WalletForm(forms.ModelForm):
    class Meta:
        model = Wallet
        exclude = ['user']


class WalletTransactionForm(forms.Form):
    from_wallet = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        required=True,
        label="From Wallet",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    to_wallet = forms.ModelChoiceField(
        queryset=Wallet.objects.all(),
        required=True,
        label="To Wallet",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label="Amount",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    rate = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=True,
        label="Rate",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

