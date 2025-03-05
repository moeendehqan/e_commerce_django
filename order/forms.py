from django import forms
from user.models import Address


class CheckoutForm(forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(),
        widget=forms.Select(attrs={'class': 'w-full p-3 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500'}),
        label="آدرس ارسال",
        empty_label="هیچ آدرسی ثبت نشده است"
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['address'].queryset = Address.objects.filter(user=user)