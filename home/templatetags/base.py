# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist

from users.models import UserInfo, Chatroom, Message

register = template.Library()

@register.filter
def getUserNickname(user):
    try:
        info = UserInfo.objects.get(user=user)
    except ObjectDoesNotExist:
        return user.username
    else:
        return info.nickname


@register.filter
@stringfilter
def get_msgs(room_id):
    room = Chatroom.objects.get(id=room_id)
    msgs = Message.objects.filter(belong_to=room)
    return msgs

# @register.filter
# def get_room_name(room_id, user_id):
#     room = Chatroom.objects.get(id=room_id)
#     user = User.objects.get(id=user_id)
#     if user == room.talker1:
#         return getUserNickname(room.talker2)
#     else:
#         return getUserNickname(room.talker1)