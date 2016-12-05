import random
from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.views.generic import ListView
from hotel.models import RoomType, Guest, Order, RoomItem, Item, StockItem, Room, Occupation, Complaint, Employee
from .forms import ContactForm, RegisterGuestForm, OrderForm, PayRoomForm, RegisterComplaintForm, EditRoomDetailForm, GuestOrderForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context, loader
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, IntegerField, Count, F
from datetime import date, timedelta


def home(request):
    context={}
    return render(request, 'hotel/home.html', context)

def about(request):
    context={}
    return render(request, 'hotel/about.html', context)

def service(request):
    context={}
    return render(request, 'hotel/service.html', context)

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
        print(context)
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

class ListComplaintsView(ListView):

    model = Complaint
    queryset = Complaint.objects.all()
    template_name = 'hotel/complaints.html'

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
            room_item=RoomItem(guest = guest, room = guest.room, date_from = guest.checkin_date, date_to = guest.checkout_date)
            room_item.save()
            if guest.checkout_date:
                delta = guest.checkout_date - guest.checkin_date
                for i in range(delta.days):
                    dt = guest.checkin_date + timedelta(days=i)
                    occ = Occupation(room = guest.room, date = dt, is_occupaid = True)
                    occ.save()
            else:
                occ = Occupation(room = guest.room, date = guest.checkin_date, is_occupaid = True)
                occ.save()


            #post.published_date = timezone.now()
            return redirect('guests')
    else:
            form = RegisterGuestForm()
    context = {'form': form}
    return render(request, 'hotel/register_guest.html', context)

@login_required
def guest_detail(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    old_checkout = guest.checkout_tracker.previous('checkout_date')
    # Order Management:
    open_orders = Order.objects.filter(guest = guest, is_paid=False)
    item_dates = open_orders.values('date')
    item_date = item_dates.order_by('date').distinct('date')
    open_bill  = []
    for d in item_date:
        open_orders = open_orders.filter(date=d['date'])
        item_ids = open_orders.values('item__name')
        item_id = item_ids.order_by('item__name').distinct('item__name')
        for i in item_id:
            q=open_orders.filter(item__name=i['item__name'], date=d['date'])
            ta=q.aggregate(total_amount =Sum('amount'))
            tp=q.aggregate(total_price = Sum('price'))
            open_bill.append({'date': d['date'], 'item': i['item__name'], 'amount': ta['total_amount'], 'price': tp['total_price']})
    unpaid_total = open_orders.aggregate(Sum('price', output_field=IntegerField()))
    unpaid_guest = guest.pk
    paid_orders = Order.objects.filter(guest = guest, is_paid=True)
    # Room Details
    room = RoomItem.objects.get(guest = guest)
    room.room = guest.room
    if guest.checkout_date:
        delta = guest.checkout_date - guest.checkin_date
        room.delta = delta.days
    else:
        room.date_to = timezone.now().strftime('%Y-%m-%d')
        delta = timezone.now().date() - guest.checkin_date
        room.delta = delta.days

    room.price = (delta.days - room.days_paid) * guest.room.room_type.price * (1-(guest.discount/100))
    room.save()






    context = {'guest': guest}
    context['open_orders'] = open_orders
    context['open_bill'] = open_bill
    context['unpaid_total'] = unpaid_total
    context['unpaid_guest'] = unpaid_guest
    context['paid_orders'] = paid_orders
    context['room'] = room

    return render(request, 'hotel/guest_detail.html', context)

@login_required
def guest_edit(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    # Form and Context data
    if request.method == "POST":
        form = RegisterGuestForm(request.POST, instance=guest,checkin_date__disabled=True)
        form.checkin_date(disabled=True)
        if form.is_valid():
            guest = form.save(commit=False)
            guest.save()
            return redirect('guest_detail', pk=guest.pk)
    else:
            form = RegisterGuestForm(instance=guest)#,checkin_date__disabled=True)

    context = {'form': form}

    return render(request, 'hotel/guest_edit.html', context)


@login_required
def guest_edit_stay(request, pk):
    guest = get_object_or_404(Guest, pk=pk)
    room_item = RoomItem.objects.get(date_to__gte = timezone.now().date(), guest=guest)
    print(room_item)
    print(request.POST)



    # Form and Context data
    if request.method == "POST":
        form = EditRoomDetailForm(request.POST, instance=room_item)
        if form.is_valid():
            print("POST mate")
            room_item = form.save(commit=False)
            room_item.save()

            print(room_item.date_to)
            print(guest.checkout_date)

            if room_item.date_to > guest.checkout_date:
                delta = room_item.date_to - guest.checkout_date
                for i in range(delta.days):
                    dt = guest.checkout_date + timedelta(days=i)
                    occ = Occupation(room = guest.room, date = dt, is_occupaid = True)
                    print(occ)
                    occ.save()

            elif guest.checkout_date > room_item.date_to:
                delta =  guest.checkout_date - room_item.date_to
                for i in range(delta.days):
                    dt = room_item.date_to + timedelta(days=i)
                    occ = Occupation.objects.get(room = guest.room, date = dt, is_occupaid = True)
                    occ.delete()

            guest.checkout_date = room_item.date_to
            guest.save()

            return redirect('guest_detail', pk=guest.pk)
    else:
        print("nix POST mate")
        form = EditRoomDetailForm(instance=room_item)





    context = {'form': form}
    return render(request, 'hotel/guest_edit_stay.html', context)

@login_required
def register_order(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.price = order.amount * order.item.price
            order.save()
            stock = StockItem.objects.get(item=order.item)
            stock.in_stock -= order.amount
            stock.save()
            #post.published_date = timezone.now()
            return redirect('guests')

    else:
            form = OrderForm()

    context = {'form': form}
    return render(request, 'hotel/order.html', context)



@login_required
def register_guest_order(request, pk, *args, **kwargs):

    guest = Guest.objects.get(pk=pk)

    if request.method == "POST":
        print("POST")
        form = GuestOrderForm(request.POST)
        if form.is_valid():
            order_save = form.save(commit=False)
            order = order_save(guest=guest)
            order.price = order.amount * order.item.price
            order.save()
            stock = StockItem.objects.get(item=order.item)
            stock.in_stock -= order.amount
            stock.save()
            #post.published_date = timezone.now()
            return redirect('guests')
    else:
        print("Nix POST Maserfagger")
        form = GuestOrderForm()

    context = {'form': form}
    return render(request, 'hotel/order.html', context)


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

@login_required
def pay_room(request, *args, **kwargs):
    form_class = PayRoomForm

    if request.method == "POST":
        guest = Guest.objects.get(pk=kwargs['pk'])
        form2 = form_class(request.POST, {'guest':guest})
        room_item = RoomItem.objects.get(guest=kwargs['pk'])
        room = RoomItem.objects.get(guest=kwargs['pk'])
        item = Item.objects.get(name='Room Rate')
        paid = room.days_paid * guest.room.room_type.price * (1-(guest.discount/100))
        if form2.is_valid():
            room_item.days_paid += form2.cleaned_data['days_paid']
            room_item.save()
            price = form2.cleaned_data['days_paid'] * guest.room.room_type.price * (1-(guest.discount/100))
            order = Order(guest = guest, amount = '1', item = item, price = price, is_paid = True, paid_date = timezone.now())
            order.save()
            #change days_paid
            return redirect('guest_detail', pk=kwargs['pk'])
    else:
        form = PayRoomForm()

    return render(request, 'hotel/pay_room.html', {'form': form})

@login_required
def room_overview(request, year, month):
    rooms = Room.objects.all()
    guests = Guest.objects.active()
    #next and previous month
    if month=='12':
        next_month='01'
        next_year=str(int(year)+1)
        previous_month=str(int(month)-1)
        if len(previous_month) == 1:
            previous_month = '0'+ previous_month
        previous_year=year
    elif month == '01':
        next_month=str(int(month)+1)
        if len(next_month) == 1:
            next_month = '0'+ next_month
        next_year=year
        previous_month='12'
        previous_year=str(int(year)-1)
    else:
        next_month=str(int(month)+1)
        if len(next_month) == 1:
            next_month = '0'+ next_month
        next_year=year
        previous_month=str(int(month)-1)
        if len(previous_month) == 1:
            previous_month = '0'+ previous_month
        previous_year=year
    #occupation calculation
    occupation = Occupation.objects.filter(date__year = year, date__month=month)
    long_month = ['01', '03', '05', '07', '08', '10', '12']
    short_month = ['04','06','09','11']
    if month in long_month:
        month_max = 31
    elif month in short_month:
        month_max = 30
    elif int(year) % 4 == 0 and int(year) %100 != 0 or int(year) % 400 == 0:
        month_max = 29
    else:
        month_max = 28

    days = []
    for i in range(1, month_max + 1):
        i = str(i)
        if len(i)==1:
            i="0"+i
        days.append(str(i))

    days_int = []
    for i in range(1, month_max + 1):
        days_int.append(i)

    context = {}

    room01 = []
    room02 = []
    room03 = []
    room04 = []
    room05 = []
    room06 = []
    room07 = []
    room08 = []
    room09 = []

    for day in days:
        if occupation.filter(date__day = day, room="1").exists():
            room01.append('1')
        else:
            room01.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="2").exists():
            room02.append('1')
        else:
            room02.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="3").exists():
            room03.append('1')
        else:
            room03.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="4").exists():
            room04.append('1')
        else:
            room04.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="5").exists():
            room05.append('1')
        else:
            room05.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="6").exists():
            room06.append('1')
        else:
            room06.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="7").exists():
            room07.append('1')
        else:
            room07.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="8").exists():
            room08.append('1')
        else:
            room08.append('0')
    for day in days:
        if occupation.filter(date__day = day, room="9").exists():
            room09.append('1')
        else:
            room09.append('0')


    context['month_max'] = range(1,month_max)
    context['room01'] =  room01
    context['room02'] =  room02
    context['room03'] =  room03
    context['room04'] =  room04
    context['room05'] =  room05
    context['room06'] =  room06
    context['room07'] =  room07
    context['room08'] =  room08
    context['room09'] =  room09
    context['rooms'] = rooms
    context['days'] = days
    context['days_int'] = days_int
    context['month'] = month
    context['year'] = year
    context['next_month']= next_month
    context['next_year'] = next_year
    context['previous_month'] = previous_month
    context['previous_year'] = previous_year

    print (context)

    return render(request, 'hotel/overview.html', context)

@login_required
def inventory(request):
    context = {}
    orders = Order.objects.exclude(item__name = 'Room Rate')
    stock = StockItem.objects.exclude(item__name = 'Room Rate')
    item_dates = orders.values('date')
    item_date = item_dates.order_by('date').distinct('date')
    inventory  = []
    for d in item_date:
        p=Order.objects.filter(date=d['date']).exclude(item__name = 'Room Rate')
        item_ids = p.values('item__name')
        item_id = item_ids.order_by('item__name').distinct('item__name')
        for i in item_id:
            q=Order.objects.filter(item__name=i['item__name'], date=d['date'])
            ta=q.aggregate(total_amount =Sum('amount'))
            tp=q.aggregate(total_price = Sum('price'))
            inventory.append({'date': d['date'], 'item': i['item__name'], 'amount': ta['total_amount'], 'price': tp})
    #Stock Calculations
    stock_items = stock.values('item')
    for i in stock_items:
        item = stock.get(item=i['item'])
        if item.in_stock <= 0:
            item.warning = 2
        elif item.in_stock - (2 * item.daily_use_avg) <=0:
            item.warning = 1
        print(item.warning)
    context['stock'] = stock
    context['inventory'] = inventory
    return render (request, 'hotel/inventory.html', context)

@login_required
def register_complaint(request):
    if request.method == "POST":
        form = RegisterComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.save()
            return redirect('complaints')
    else:
            form = RegisterComplaintForm()
    context = {'form': form}
    return render(request, 'hotel/register_complaint.html', context)
