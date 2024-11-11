from django import template
from chat.models import Message, ChatRoom

register = template.Library()

@register.filter
def unread_messages(user, current_user):
    # Trouver la salle de chat entre les deux utilisateurs
    chat_room = ChatRoom.objects.filter(
        participants=current_user,
        is_group=False
    ).filter(participants=user).first()
    
    if chat_room:
        # Compter les messages non lus
        return Message.objects.filter(
            chat_room=chat_room,
            sender=user,
            is_read=False
        ).count()
    return 0

@register.filter
def last_message(user, current_user):
    # Trouver la salle de chat entre les deux utilisateurs
    chat_room = ChatRoom.objects.filter(
        participants=current_user,
        is_group=False
    ).filter(participants=user).first()
    
    if chat_room:
        # Retourner le dernier message
        return Message.objects.filter(chat_room=chat_room).last()
    return None 