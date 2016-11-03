from django.shortcuts import render, render_to_response, redirect
from django.views.generic import ListView
from hotel.models import RoomType
from .forms import ContactForm
from django.template.loader import get_template
from django.core.mail import EmailMessage
from django.template import Context

def home(request):
    return render_to_response('hotel/home.html')



class ListRoomsView(ListView):

    model = RoomType
    template_name = 'hotel/rooms.html'

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
