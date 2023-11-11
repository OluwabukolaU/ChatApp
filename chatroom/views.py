from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import ChatRoom

# Create your views here.

@login_required
def chatrooms(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chatroom/chatrooms.html', {'chatrooms': chatrooms})

@login_required
def chatroom(request, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    return render(request, 'chatroom/chatroom.html', {'chatroom': chatroom})
