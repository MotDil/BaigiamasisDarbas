from django import forms
from django.forms.models import inlineformset_factory
from .models import IssuedInvoice, ReceivedInvoice, IssuedInvoiceLine


class IssuedInvoiceForm(forms.ModelForm):
    class Meta:
        model = IssuedInvoice
        fields = '__all__'


IssuedInvoiceLineFormSet = inlineformset_factory(
    IssuedInvoice,
    IssuedInvoiceLine,
    fields=('id', 'product', 'quantity', 'price'),
    extra=5,
    can_delete=True,
)


class ReceivedInvoiceForm(forms.ModelForm):
    class Meta:
        model = ReceivedInvoice
        fields = '__all__'
