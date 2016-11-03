from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^rooms/$', views.ListRoomsView.as_view(), name='rooms'),
    url(r'^contact/$', views.contact, name='contact'),
    ]