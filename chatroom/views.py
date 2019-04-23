from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings

from django.db.models import Q

from commodity.models import Commodity
from chatroom.models import Chatroom, Chatmsg
from helper.decorator import user_verify_required

import re, time, json

@login_required
@user_verify_required
def room_list(request):
    rooms = Chatroom.objects.filter(Q(member1=request.user)|Q(member2=request.user))
    context = { 'rooms': rooms }
    return render(request, 'chatroom/room_list.html', context)


# {% url 'chatroom:start_chat' comm.owner.id comm.id %}
@login_required
@user_verify_required
def start_chat(request, user_id, comm_id):
    if request.user.id == user_id:
        response_data = {
            'message': "你就是卖家啦，不能创建与自己的聊天室哦",
            'next_page': "聊天列表",
            'goto_url': settings.CUR_HOST + 'chatroom/room_list/',
            'goto_time': 5,
        }
        return render(request, 'users/message.html' , response_data)

    member2 = User.objects.get(id=user_id)
    comm = Commodity.objects.get(id=comm_id)
    rooms = Chatroom.objects.filter(member1=request.user, member2=member2, commodity=comm)
    if len(rooms) == 0:
        room = Chatroom.objects.create(member1=request.user, member2=member2, commodity=comm)
    else:
        room = rooms[0]
        room.mem1_del = False
        room.mem2_del = False
        room.save()

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

    if room.member1 == request.user:
        room.mem1_read = True
    elif room.member2 == request.user:
        room.mem2_read = True
    room.save()

    if request.method == 'POST':
        text = request.POST['text'].strip()
        image = request.FILES.get('image', None)
        
        if text.strip() != '' or image:
            Chatmsg.objects.create(room=room, sender=request.user, content=text, image=image)
        
        if room.member1 == request.user:
            room.mem2_read = False
        elif room.member2 == request.user:
            room.mem1_read = False
        room.save()

        # 这里使用reverse可以避免出现刷新后表单重复提交的问题
        return HttpResponseRedirect(reverse('chatroom:room_detail', kwargs={'room_id': room.id}))

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

    last_id = request.GET.get('last', 0)

    messages = Chatmsg.objects.filter(room=room).filter(id__gt=last_id)

    context = { 'messages': messages }
    return render(request, 'chatroom/message.html', context)
    

@login_required
def del_room(request, room_id, mem_id):
    room = Chatroom.objects.get(id=room_id)
    if request.user != room.member1 and request.user != room.member2:
        raise Http404

    if mem_id == room.member1.id:
        room.mem1_del = True
    if mem_id == room.member2.id:
        room.mem2_del = True
    room.save()
    if room.mem1_del and room.mem2_del:
        room.delete()
    return HttpResponseRedirect(reverse('chatroom:room_list'))

def chat_intro(request):
    return render(request, 'chatroom/chat_intro.html')