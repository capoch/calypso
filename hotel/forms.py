from django import forms
from .models import Guest, Order, Item
from django.contrib.admin import widgets


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True)
    contact_email = forms.EmailField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].label = "Your name:"
        self.fields['contact_email'].label = "Your email:"
        self.fields['content'].label = "What do you want to say?"

class RegisterGuestForm(forms.ModelForm):

    class Meta:
        model = Guest
        fields = ('checkin_date', 'checkout_date', 'gender', 'name', 'email', 'passport_number', 'passport_deposited', 'motorcycle', 'room')

    def __init__(self, *args, **kwargs):
        super(RegisterGuestForm, self).__init__(*args, **kwargs)
        self.fields['checkin_date'].widget = widgets.AdminDateWidget()

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('guest', 'item', 'amount')
