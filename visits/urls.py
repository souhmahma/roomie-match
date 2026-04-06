from django.urls import path
from . import views

app_name = 'visits'

urlpatterns = [
    path('my-visits/',                          views.my_visits,           name='my_visits'),
    path('manage/',                             views.manage_visits,        name='manage'),
    path('request/<int:listing_pk>/',           views.request_visit,        name='request'),
    path('<int:pk>/<str:action>/',              views.update_visit_status,  name='update_status'),
    path('cancel/<int:pk>/',                    views.cancel_visit,         name='cancel'),
    path('availability/<int:listing_pk>/',      views.manage_availability,  name='availability'),
]