from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('',                     views.inbox,               name='inbox'),
    path('<int:pk>/',             views.conversation_detail, name='conversation'),
    path('start/<int:user_pk>/',  views.start_conversation,  name='start'),
    path('unread/',               views.unread_count,         name='unread_count'),
]