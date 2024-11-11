from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('chat/<int:room_id>/', views.chat_room, name='chat_room'),
    path('chat/<int:room_id>/send/', views.send_message, name='send_message'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('start-chat/<int:user_id>/', views.start_chat, name='start_chat'),
] 