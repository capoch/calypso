from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from hotel.models import RoomType, Guest, Order, RoomItem
from .forms import ContactForm, RegisterGuestForm, OrderForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, IntegerField, Count
from datetime import date


def home(request):
    return render_to_response('hotel/home.html')

def about(request):
    return render_to_response('hotel/about.html')

def service(request):
    return render_to_response('hotel/service.html')

class ListRoomsView(ListView):

    model = RoomType
    template_name = 'hotel/rooms.html'

class ListGuestsView(ListView):

    model = Guest

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ListGuestsView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['active'] = Guest.objects.active()
        context['reservation'] = Guest.objects.future()
        return context

    template_name = 'hotel/guests.html'

class ListReservationsView(ListView):

    model = Guest
    queryset = Guest.objects.future()
    template_name = 'hotel/guests.html'

class ListOrdersView(ListView):

    model = Order
    queryset = Order.objects.filter(is_paid = False)
    template_name = 'hotel/open_orders.html'

class ListGuestOrdersView(ListView):

    model = Order
    queryset = Order.objects.filter(is_paid = False)
    template_name = 'hotel/guest_detail.html'
    def get_context_data(self, pk):
    # Call the base implementation first to get a context
        context = super(ListOrdersView, self).get_context_data(pk)
    # Add in the publisher
        context['guest'] = self.guest.pk
        return context
# Create your views here.
def contact(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get(
                'contact_name'
            , '')
            contact_email = request.POST.get(
                'contact_email'
            , '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('hotel/contact_template.txt')
            context = Context({
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
            })
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['youremail@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()

            return redirect('contact')

    return render(request, 'hotel/contact.html', {
        'form': form_class,
    })

@login_required
def register_guest(request):
    if request.method == "POST":
        form = RegisterGuestForm(request.POST)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.save()
            #post.published_date = timezone.now()
            return redirect('guests')
    else:
            form = RegisterGuestForm()
    context = {'form': form}
    return render(request, 'hotel/guest_detail.html', context)

@login_required
def guest_detail(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
# Order Management:
    open_orders = Order.objects.filter(guest = guest, is_paid=False)
    open_bill = open_orders.values('date','item').annotate(Sum('amount')).annotate(Sum('price'))
    unpaid_total = open_orders.aggregate(Sum('price', output_field=IntegerField()))
    unpaid_guest = guest.pk
    paid_orders = Order.objects.filter(guest = guest, is_paid=True)
# Room Details
    room = RoomItem.objects.filter(guest = guest)
    room.room = guest.room
    room.date_from = guest.checkin_date.strftime('%Y-%m-%d')
    room.date_to = timezone.now().strftime('%Y-%m-%d')
    #todo: account for when date_to is checkout in the future
    delta = timezone.now().date() - guest.checkin_date
    room.price = delta.days * guest.room.room_type.price
# Form and Context data
    if request.method == "POST":
        form = RegisterGuestForm(request.POST, instance=guest)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.save()
            return redirect('guest_detail', pk=guest.pk)
    else:
            form = RegisterGuestForm(instance=guest)
    context = {'form': form}
    context['open_orders'] = open_orders
    context['open_bill'] = open_bill
    context['unpaid_total'] = unpaid_total
    context['unpaid_guest'] = unpaid_guest
    context['paid_orders'] = paid_orders
    context['room'] = room
    return render(request, 'hotel/guest_detail.html', context)


@login_required
def register_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.price = order.amount * order.item.price
            order.save()
            #post.published_date = timezone.now()
            return redirect('new_order')

    else:
            form = OrderForm()
    context = {'form': form}
    return render(request, 'hotel/order.html', context)



@login_required
def register_guest_order(request,go):

    if request.method == "POST":
        form = RegisterGuestForm(request.POST, initial={'guest': go})
        if form.is_valid():
            guest = form.save(commit=False)
            guest.save()
            #post.published_date = timezone.now()
            return redirect('guests')
    else:
            return redirect ('ListOrdersView')
    context = {'form': form}
    return render(request, 'hotel/guest_detail.html', context)


@login_required
def order_detail(request, pk):
    guest = get_object_or_404(Order, pk=pk)
    if request.method == "POST":
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.save()
            #post.published_date = timezone.now()
            return redirect('order', pk=guest.pk)
    else:
            form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'hotel/order.html', context)

@login_required
def pay_order(request, *args, **kwargs):
    order = Order.objects.get(pk=kwargs['pk'])
    if order.is_paid is False:
        order.is_paid = True
        order.paid_date = timezone.now()
        order.save()
    return redirect(guest_detail, pk=kwargs['go'])

@login_required
def pay_total(request, *args, **kwargs):
    orders = Order.objects.filter(guest=kwargs['go'])
    for order in orders:
        if order.is_paid is False:
            order.is_paid = True
            order.paid_date = timezone.now()
            order.save()
    return redirect(guest_detail, pk=kwargs['go'])
