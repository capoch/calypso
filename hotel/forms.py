from django import forms
from .models import Guest, Order, Item, RoomItem
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
    checkin_date = forms.DateField(widget=forms.SelectDateWidget)
    checkout_date = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = Guest
        fields = ('checkin_date', 'checkout_date', 'gender', 'name', 'email', 'passport_number', 'passport_deposited', 'motorcycle', 'room', 'discount')

    def __init__(self, *args, **kwargs):
        super(RegisterGuestForm, self).__init__(*args, **kwargs)
        self.fields['checkin_date'].widget = widgets.AdminDateWidget()

    def clean(self):
        cleaned_data = super(RegisterGuestForm, self).clean()
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        name = cleaned_data.get("name")
        passport_number = cleaned_data.get("passport_number")
        discount = cleaned_data.get("discount")

        if checkin_date and name and passport_number:
            # Only do something if both fields are valid so far.
            if checkout_date:
                if checkout_date <= checkin_date:
                    raise forms.ValidationError("Checkout date must be after check-in date.")
            elif len(name)<=5:
                raise forms.ValidationError("Please enter full name")
            elif len(passport_number)<=5:
                raise forms.ValidationError("Please enter correct Passport Number")


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('guest', 'item', 'amount')

class PayRoomForm(forms.Form):
    guest = forms.ModelMultipleChoiceField(queryset=Guest.objects.all())
    days_paid = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(PayRoomForm, self).__init__(*args, **kwargs)
        self.fields['days_paid'].label = "Number of days:"


    class Meta:
        model = RoomItem
