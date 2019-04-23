# -*- coding: utf-8 -*-
import markdown
import markdownx

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.core.exceptions import ObjectDoesNotExist

from users.models import UserInfo

register = template.Library()

@register.filter(is_safe = True)
@stringfilter
def custom_markdown(value):
    return mark_safe(markdown.markdown(value,
                              extensions = ['markdown.extensions.extra',
                                            'markdown.extensions.toc',
                                            'markdown.extensions.sane_lists',
                                            'markdown.extensions.nl2br',
                                            'markdown.extensions.codehilite',],
                              safe_mode = True,
                              enable_attributes = False))

@register.filter
def getUserNickname(user):
    try:
        info = UserInfo.objects.get(user=user)
    except ObjectDoesNotExist:
        return user.username
    else:
        return info.nickname

@register.filter
def is_del(room, user):
    if room.member1 == user and room.mem1_del:
        return False
    if room.member2 == user and room.mem2_del:
        return False
    return True

@register.filter
def getVerifyStatus(user):
    try:
        info = UserInfo.objects.get(user=user)
    except ObjectDoesNotExist:
        return False    
    return info.is_verify
