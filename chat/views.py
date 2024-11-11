from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import ChatRoom, Message, UserProfile
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User

@login_required
def chat_list(request):
    chat_rooms = ChatRoom.objects.filter(participants=request.user)
    available_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/chat_list.html', {
        'chat_rooms': chat_rooms,
        'available_users': available_users
    })

@login_required
def chat_room(request, room_id):
    chat_room = ChatRoom.objects.get(id=room_id)
    messages = Message.objects.filter(chat_room=chat_room)
    
    # Marquer les messages non lus comme lus
    Message.objects.filter(
        chat_room=chat_room,
        sender__in=chat_room.participants.exclude(id=request.user.id),
        is_read=False
    ).update(is_read=True)
    
    return render(request, 'chat/chat_room.html', {
        'chat_room': chat_room,
        'messages': messages
    })

@login_required
def send_message(request, room_id):
    if request.method == 'POST':
        content = request.POST.get('content')
        file = request.FILES.get('file')
        chat_room = ChatRoom.objects.get(id=room_id)
        
        message = Message.objects.create(
            chat_room=chat_room,
            sender=request.user,
            content=content,
            file=file
        )
        
        return JsonResponse({
            'status': 'success',
            'message_id': message.id,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        })
    return JsonResponse({'status': 'error'})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:chat_list')
    else:
        form = UserCreationForm()
    return render(request, 'chat/auth/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('chat:chat_list')
    else:
        form = AuthenticationForm()
    return render(request, 'chat/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('chat:login')

@login_required
def start_chat(request, user_id):
    other_user = User.objects.get(id=user_id)
    
    existing_chat = ChatRoom.objects.filter(
        participants=request.user,
        is_group=False
    ).filter(participants=other_user).first()
    
    if existing_chat:
        chat_room = existing_chat
    else:
        chat_room = ChatRoom.objects.create(
            name=f"Chat avec {other_user.username}",
            is_group=False
        )
        chat_room.participants.add(request.user, other_user)
        
    return redirect('chat:chat_room', room_id=chat_room.id)
