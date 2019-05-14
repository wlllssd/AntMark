from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from helper.decorator import superuser_required

from commodity.models import Commodity
from users.models import UserInfo, Message
from admin_manage.models import Announcement

@login_required
@superuser_required
def admin_index(request):
    return render(request, 'admin_manage/index.html')

@login_required
@superuser_required
def stu_verify_list(request):
    # 这里默认只能是管理员才能登陆, request.user即为管理员
    inbox_messages = Message.objects.filter(receiver=request.user, 
        msg_type='stu_verify', receiver_del=False).order_by('-timestamp')
    outbox_messages = Message.objects.filter(sender=request.user, 
        msg_type='stu_verify', sender_del=False).order_by('-timestamp')
    context = {
        'function': "学生认证",
        'inbox_messages': inbox_messages,
        'outbox_messages': outbox_messages
    }
    return render(request, 'admin_manage/sp_mailbox.html', context)

@login_required
@superuser_required
def comm_verify_list(request):
    inbox_messages = Message.objects.filter(receiver=request.user, 
        msg_type='commodity_verify', receiver_del=False).order_by('-timestamp')
    outbox_messages = Message.objects.filter(sender=request.user, 
        msg_type='commodity_verify', sender_del=False).order_by('-timestamp')
    context = {
        'function': "商品",
        'inbox_messages': inbox_messages,
        'outbox_messages': outbox_messages
    }
    return render(request, 'admin_manage/sp_mailbox.html', context)


@login_required
@superuser_required
def stu_verify_detail(request, message_id, user_id):
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        stu_user = User.objects.get(id=user_id)
        stu_info = UserInfo.objects.get(user=stu_user)
    except ObjectDoesNotExist:
        raise Http404
    
    if stu_info.is_verified == True:
        response_data = {
            'message': "该用户已经完成学生验证",
            'next_page': "学生认证管理页面",
            'goto_url': settings.CUR_HOST + 'admin_manage/stu_verify_list',
            'goto_time': 3,
        }
        return render(request, 'users/notice.html' , response_data)

    if request.method == 'POST':
        text = request.POST['text']
        if 'verified' in request.POST:
            stu_info.is_verified = True
            stu_info.save()
        text = '【学生认证审核】 ' + text
        Message.objects.create(sender=request.user, receiver=stu_user, text=text)
        return HttpResponseRedirect(reverse('admin_manage:stu_verify_list'))

    context = { 
        'message': message,
        'stu_user': stu_user,
        'stu_info': stu_info,
    }
    return render(request, 'admin_manage/stu_verify_detail.html', context)    


@login_required
@superuser_required
def comm_verify_detail(request, message_id, comm_id):
    try:
        message = Message.objects.get(id=message_id)
        message.is_read = True
        message.save()
        comm = Commodity.objects.get(id=comm_id)
    except ObjectDoesNotExist:
        raise Http404

    if comm.is_verified == True:
        response_data = {
            'message': "商品已经完成审核，无须再次审核",
            'next_page': "商品审核管理页面",
            'goto_url': settings.CUR_HOST + 'admin_manage/comm_verify_list',
            'goto_time': 3,
        }
        return render(request, 'users/notice.html' , response_data)

    if request.method == 'POST':
        text = request.POST['text']
        if 'verified' in request.POST:
            comm.is_verified = True
            comm.save()
        text = '【商品审核】 你的商品 [' + comm.title + '] 的审核结果 ' + text
        Message.objects.create(sender=request.user, receiver=comm.owner, text=text)
        return HttpResponseRedirect(reverse('admin_manage:comm_verify_list'))

    context = {
        'message': message, 
        'comm': comm,
        }
    return render(request, 'admin_manage/comm_verify_detail.html', context)


@login_required
@superuser_required
def create_anno(request):
    """ 管理员发布公告 """
    if request.method == 'POST':
        response_data = {
            'message': "公告内容不可为空",    
            'next_page': "管理员后台主页",
            'goto_url': settings.CUR_HOST + 'admin_manage',
            'goto_time': 2,
        }
        title = request.POST['title']
        text = request.POST['text']
        if text:
            Announcement.objects.create(text=text, title = title)
            response_data['message'] = "你已创建新的公告"        
        return render(request, 'users/notice.html' , response_data)

    return render(request, 'admin_manage/create_anno.html')


@login_required
@superuser_required
def read_message(request, message_id):
    """ 阅读消息完整内容 """
    message = Message.objects.get(id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        message.save()

    context = { 'message': message }
    return render(request, 'admin_manage/sp_read_message.html', context)


@login_required
@superuser_required
def del_message(request, message_id):
    """ 某方删除当前消息，若另一方已删除，则删除该信息 """
    try:
        del_message = Message.objects.get(id=message_id)
    except ObjectDoesNotExist:
        raise Http404
    if del_message.msg_type == 'stu_verify':           
        del_message.delete()
        return HttpResponseRedirect(reverse('admin_manage:stu_verify_list'))
    elif del_message.msg_type == 'commodity_verify':
        del_message.delete()
        return HttpResponseRedirect(reverse('admin_manage:comm_verify_list'))


@login_required
@superuser_required
def deal_mult_msg(request):
    msg_ids = request.POST.getlist("checkbox_list")
    if 'delete_msg' in request.POST:
        for idx in msg_ids:
            response = del_message(request, int(idx))
    if 'response' in locals().keys():
        return response
    return HttpResponseRedirect(reverse('users:mail_inbox'))