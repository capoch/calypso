from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^rooms/$', views.ListRoomsView.as_view(), name='rooms'),
    url(r'^service/$', views.service, name='service'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^about/$', views.about, name='about'),
    url(r'^guests/$', views.ListGuestsView.as_view(), name='guests'),
    url(r'^guests/detail/(?P<pk>\d+)/$', views.guest_detail, name='guest_detail'),
    url(r'^guests/edit/(?P<pk>\d+)/$', views.guest_edit, name='guest_edit'),
    url(r'^guests/edit/room/(?P<pk>\d+)/$', views.guest_edit_stay, name='guest_edit_stay'),
    url(r'^guests/room/(?P<pk>\d+)/$', views.pay_room, name='pay_room'),
    url(r'^register_guest/$', views.register_guest, name='register_guest'),
    url(r'^order/edit/(?P<pk>\d+)/$', views.order_detail, name='order'),
    url(r'^order/$', views.register_order, name='new_order'),
    url(r'^guests/(?P<pk>\d+)/order/$', views.register_guest_order, name='new_guest_order'),
    url(r'^order/list/$', views.ListOrdersView.as_view(), name='open_orders'),
    url(r'^order/pay/(?P<pk>\d+)/(?P<go>\d+)/$', views.pay_order, name='pay_order'),
    url(r'^order/pay/total/(?P<go>\d+)/$', views.pay_total, name='pay_total'),
    url(r'^room/overview/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.room_overview, name='room_overview'),
    url(r'^inventory/$', views.inventory, name='inventory'),
    url(r'^register_complaint/$', views.register_complaint, name='register_complaint'),
    url(r'^complaints/$', views.ListComplaintsView.as_view(), name='complaints'),


    ]
