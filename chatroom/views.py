from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Q

from commodity.models import Commodity
from chatroom.models import Chatroom, Chatmsg

import re, time, json
from django.core import serializers

@login_required
def room_list(request):
    rooms = Chatroom.objects.filter(Q(member1=request.user)|Q(member2=request.user))
    context = { 'rooms': rooms }
    return render(request, 'chatroom/room_list.html', context)

# {% url 'chatroom:start_chat' comm.owner.id comm.id %}
@login_required
def start_chat(request, user_id, comm_id):
    member2 = User.objects.get(id=user_id)
    comm = Commodity.objects.get(id=comm_id)
    try:
        room = Chatroom.objects.get(member1=request.user, member2=member2)
        room.commodity = comm
        room.save()
    except ObjectDoesNotExist:
        room = Chatroom.objects.create(menber1=request.user, member2=member2, commodity=comm)
    
    messages = Chatmsg.objects.filter(room=room)

    context = { 
        'room' : room,
        'messages': messages,
    }
    return render(request, 'chatroom/room_detail.html', context)

@login_required
def room_detail(request, room_id):
    room = Chatroom.objects.get(id=room_id)
    if request.user != room.member1 and request.user != room.member2:
        raise Http404

    if request.method == 'POST':
        text = request.POST['text'].strip()
        image = request.FILES.get('image', None)
        
        if text.strip() != '' or image:
            Chatmsg.objects.create(room=room, sender=request.user, content=text, image=image)

    messages = Chatmsg.objects.filter(room=room)

    context = { 
        'room': room,
        'messages': messages,
    }
    return render(request, 'chatroom/room_detail.html', context)

@login_required
def get_messages(request, room_id):
    room = Chatroom.objects.get(id=room_id)
    if request.user != room.member1 and request.user != room.member2:
        raise Http404

    # if request.method == 'POST':
    last_id = request.GET.get('last', 0)    
    print("last_id ======================= ", last_id)
    messages = Chatmsg.objects.filter(room=room).filter(id__gt=last_id)

    context = { 'messages': messages }
    return render(request, 'chatroom/message.html', context)
    # else:
    raise Http404
