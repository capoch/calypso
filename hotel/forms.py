from django import forms
from .models import Guest, Order, Item, RoomItem, Complaint
from django.contrib.admin import widgets
from django.utils import timezone


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
    #checkin_date = forms.DateField(widget=forms.SelectDateWidget)
    checkin_date = forms.DateField(initial=timezone.now().date())
    checkout_date = forms.DateField(initial=timezone.now().date())
    class Meta:
        model = Guest
        fields = ('checkin_date', 'checkout_date', 'name', 'email', 'passport_number', 'passport_deposited', 'motorcycle', 'room', 'discount')

    def __init__(self, *args, **kwargs):
        super(RegisterGuestForm, self).__init__(*args, **kwargs)
        self.fields['checkin_date'].widget.attrs = {'class': 'datepicker1'}

    def clean(self):
        cleaned_data = super(RegisterGuestForm, self).clean()
        checkin_date = cleaned_data.get("checkin_date")
        checkout_date = cleaned_data.get("checkout_date")
        room = cleaned_data.get('room')
        name = cleaned_data.get("name")
        passport_number = cleaned_data.get("passport_number")
        discount = cleaned_data.get("discount")
        guest = cleaned_data.get('guest')


        if checkin_date and name and passport_number:
            # Only do something if both fields are valid so far.
            if checkout_date:
                if checkout_date <= checkin_date:
                    raise forms.ValidationError("Checkout date must be after check-in date.")
            elif len(name)<=5:
                raise forms.ValidationError("Please enter full name")
            elif len(passport_number)<=5:
                raise forms.ValidationError("Please enter correct Passport Number")
        #checkin in the Past
        if not guest:
            if checkin_date < timezone.now().date():
                raise forms.ValidationError("Check-In cannot be in the past")
        #check room availability
        if RoomItem.objects.filter(room=room, date_from__lte=self.cleaned_data['checkin_date'], date_to__gt=self.cleaned_data['checkin_date']).exists() | RoomItem.objects.filter(room=room, date_from__lt=self.cleaned_data['checkout_date'], date_to__gte=self.cleaned_data['checkout_date']).exists():
            raise forms.ValidationError("Room is not available")

class EditRoomDetailForm(forms.ModelForm):
    #checkin_date = forms.DateField(widget=forms.SelectDateWidget)
    class Meta:
        model = RoomItem
        fields = ('guest','date_from', 'date_to', 'room')


    def clean(self):
        cleaned_data = super(EditRoomDetailForm, self).clean()
        guest = cleaned_data.get('guest')
        checkin_date = cleaned_data.get("date_from")
        checkout_date = cleaned_data.get("date_to")
        room = cleaned_data.get('room')



        if checkout_date:
            if checkout_date <= checkin_date:
                raise forms.ValidationError("Checkout date must be after check-in date.")

        #check room availability
        if RoomItem.objects.exclude(guest=guest).filter(room=room, date_from__lte=self.cleaned_data['date_from'], date_to__gt=self.cleaned_data['date_from']).exists() | RoomItem.objects.exclude(guest=guest).filter(room=room, date_from__lt=self.cleaned_data['date_to'], date_to__gte=self.cleaned_data['date_to']).exists():
            raise forms.ValidationError("Room is not available")

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('guest', 'item', 'amount')

    def clean(self):
        cleaned_data = super(OrderForm, self).clean()
        guest = cleaned_data.get("guest")
        item = cleaned_data.get("item")
        amount = cleaned_data.get('amount')

        
class GuestOrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ('item', 'amount')



class PayRoomForm(forms.Form):
    guest = forms.ModelMultipleChoiceField(queryset=Guest.objects.all())
    days_paid = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        super(PayRoomForm, self).__init__(*args, **kwargs)
        self.fields['days_paid'].label = "Number of days:"


    class Meta:
        model = RoomItem

class RegisterComplaintForm(forms.ModelForm):

    class Meta:
        model = Complaint
        fields = ('room', 'date_reported', 'date_fixed', 'responsible', 'severity', 'category', 'comments')
