from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives, send_mail

from django.db.models import Q

from helper.crypto import encrypt, decrypt
from django.conf import settings

from users.models import UserInfo, Message
from users.forms import InfoForm
from commodity.models import Commodity

import re, time, json

def login_view(request):
    """ 用户登录 """
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:index'))
    if request.method != 'POST':
        form = AuthenticationForm(request)
    else:
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home:index'))
    context = { 'form': form }
    return render(request, 'users/login.html', context)


def logout_view(request):
    """ 用户登出 """
    logout(request)
    return HttpResponseRedirect(reverse('home:index'))


def get_active_code(email):
    """ 利用时间及邮箱获取激活码 """
    key = 9
    encry_str = '%s|%s' % (email,time.strftime('%Y-%m-%d',time.localtime(time.time())))
    active_code = encrypt(key, encry_str)
    return active_code


def send_active_email(email, active_code):
    """ 发送激活邮件 """
    url = settings.CUR_HOST + 'users/active/' + active_code
    subject = '[AntMark]激活你的账号'
    message = '''
        <h2> <a href=''' + settings.CUR_HOST + ''' target=_blank> AntMark.com </a> </h2>
        <br/>
        <p>点击下面的链接进行激活操作（7天后过期）<a href="%s" target=_balnk> AntMark激活链接 </a></p>
    ''' % url

    send_mail(subject, '', 'antmark_mail@sina.com', [email], fail_silently=False, html_message=message)
    
    
def user_reg(request):
    response_data = {}
    user_form = UserCreationForm()
    if request.method == 'POST':
        try:
            reg_name = request.POST['username']
            reg_pwd1 = request.POST['password1']
            reg_pwd2 = request.POST['password2']

            if len(reg_name) * len(reg_pwd1) * len(reg_pwd2) == 0:
                raise Exception('邮箱或密码为空')
            
            #匹配邮箱格式
            pattern = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
            match = pattern.match(reg_name)
            if not match:
                raise Exception('邮箱格式错误')

            pattern = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$')
            match = pattern.match(reg_pwd1)
            if not match:
                raise Exception('密码必须包含大小写字母和数字的组合，可以使用特殊字符，长度在8-16之间')

            # 判断用户名是否已经被注册
            user = User.objects.filter(username=reg_name)
            if len(user) > 0:
                raise Exception('该邮箱已被注册')
            
            if reg_pwd1 != reg_pwd2:
                raise Exception('两次输入的密码不一致')

            user_form = UserCreationForm(data=request.POST)
            # if user_form.is_valid():
            new_user = user_form.save()
            new_user.email = reg_name
            new_user.is_active = False
            new_user.save()

            response_data['success'] = True
            response_data['message'] = '注册成功，已发送激活邮件到你的邮箱，请前往激活'
            
        except Exception as e:
            response_data['success'] = False
            response_data['message'] = '密码不合法，换一个试试？'
        
        finally:
            if response_data['success']:
                try:
                    active_code = get_active_code(reg_name)
                    send_active_email(reg_name, active_code)
                except Exception as e:
                    response_data['message'] = '发送激活邮件失败，请稍后重新注册' + str(e)
                    new_user.delete()
                    
                response_data['goto_url'] = settings.CUR_HOST + 'users/login'
                response_data['goto_time'] = 5
                response_data['next_page'] = "用户登录界面"
                return render(request, 'users/notice.html', response_data)
    
    context = { 
        'user_form': user_form, 
        'response_data': response_data,
    }
    return render(request, 'users/register.html' , context)


def user_active(request, active_code):
    """ 激活用户 """
    # 加错误处理，避免出错。出错认为激活链接失效
    # 解密激活链接
    key, response_data = 9, {}
    try:
        decrypt_str = decrypt(key,active_code)
        decrypt_data = decrypt_str.split('|')
        email = decrypt_data[0]                                     #邮箱
        create_date = time.strptime(decrypt_data[1], "%Y-%m-%d")    #激活链接创建日期
        create_date = time.mktime(create_date)                      #struct_time 转成浮点型的时间戳
 
        day = int((time.time()-create_date)/(24*60*60))             #得到日期差
        if day > 7:
            raise Exception(u'激活链接过期')
 
        #激活
        user = User.objects.filter(username=email)
        if len(user) == 0:
            raise Exception(u'激活链接无效')
        else:
            user = User.objects.get(username=email)
 
        if user.is_active:
            raise Exception(u'该帐号已激活过了')

        else:
            user.is_active = True
            user.save()
            # 在确认用户账号激活成功后及时创建用户信息表
            UserInfo.objects.create(user=user)
            
 
        response_data['goto_page'] = True
        response_data['message'] = '激活成功，欢迎加入AntMark！'

    except IndexError as e:
        response_data['goto_page'] = False
        response_data['message'] = '激活链接无效'
    
    except Exception as e:
        response_data['goto_page'] = False
        response_data['message'] = str(e)
    
    finally:
        #激活成功就跳转到首页(message页面有自动跳转功能)
        response_data['goto_url'] = settings.CUR_HOST + 'users/login'
        response_data['goto_time'] = 5
        response_data['next_page'] = "用户登录界面"

        return render(request, 'users/notice.html' , response_data)


@login_required
def user_settings(request):
    if request.method != 'POST':
        try:
            info = UserInfo.objects.get(user=request.user)
        except ObjectDoesNotExist:
            info = UserInfo.objects.create(user=request.user)
        info_form = InfoForm(instance=info)
        context = {
            'info_form': info_form,
            'info': info,
        }
        return render(request, 'users/settings.html' , context)
    else:
        info_form = InfoForm(data=request.POST)
        if info_form.is_valid():
            try:
                info = UserInfo.objects.get(user=request.user)
            except ObjectDoesNotExist:
                info = UserInfo.objects.create(user=request.user)
        info.nickname = info_form.cleaned_data["nickname"]
        info.gender = info_form.cleaned_data["gender"]
        info.intro = info_form.cleaned_data["intro"]
        info.phone = info_form.cleaned_data['phone']
        info.wechat = info_form.cleaned_data['wechat']
        info.qq = info_form.cleaned_data['qq']
        myprofile = request.FILES.get('profile', None)

        if myprofile:
            accept_format = ['png', 'jpg', 'peg'] #peg -> jpeg
            if myprofile.name[-3:] not in accept_format:
                response_data = {
                    'message': "提交的图片格式应该为 png/jpg/jpeg ",
                    'next_page': "用户设置页面",
                    'goto_url': settings.CUR_HOST + 'users/settings/', 
                    'goto_time': 3,
                }
                return render(request, 'users/notice.html' , response_data)
                
            if info.profile.name != 'user/img/default.jpg' :
                info.profile.delete()
            info.profile = myprofile
        info.save()
        return HttpResponseRedirect(reverse('home:index'))


@login_required
def reset_password(request):
    form = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)

            response_data = {}
            response_data['message'] = '密码修改成功，返回主页面'
            response_data['goto_url'] = settings.CUR_HOST
            response_data['goto_time'] = 3

            return render(request, 'users/notice.html' , response_data)

    context = { 'form': form }
    return render(request, 'users/reset_pwd.html', context)


@login_required
def personal_index(request, user_id):
    cur_user = User.objects.get(id=user_id)
    cur_info = UserInfo.objects.get(user=cur_user)
    comms = Commodity.objects.filter(owner=cur_user)
    context = {
        'cur_user': cur_user,
        'cur_info': cur_info,
        'comms': comms,
    }
    return render(request, 'users/personal_index.html', context)


@login_required
def stu_verify(request):
    """ 用户提交校园卡照片，后台审核 """
    info = UserInfo.objects.get(user=request.user)
    response_data = {
        'message': "你已经完成学生认证啦，不用重复认证",
        'next_page': "用户设置页面",
        'goto_url': settings.CUR_HOST + 'users/settings/', 
        'goto_time': 3,
    }
    if info.is_verified:
        return render(request, 'users/notice.html' , response_data)

    if request.method == 'POST':
        stu_card_photo = request.FILES.get('stu_card_photo', None)

        accept_format = ['png', 'jpg', 'peg'] #peg -> jpeg
        if stu_card_photo.name[-3:] not in accept_format:
            response_data['message'] = "提交的图片格式应该为 png/jpg/jpeg "
            return render(request, 'users/notice.html' , response_data)

        if stu_card_photo:
            info.stuCardPhoto = stu_card_photo
        info.save()
        
        # 发消息给管理员通知其进行审核
        text = "用户" + info.nickname + "(" + request.user.username + ")" + \
            "提交了学生身份认证文件，请尽快审核"
        admin_user = User.objects.filter(is_superuser=True)[0]
        Message.objects.create(text=text, id_content=request.user.id, 
            msg_type='stu_verify', sender=admin_user, receiver=admin_user)

        return HttpResponseRedirect(reverse('users:settings'))

    return render(request, 'users/student_verify.html')


# 消息处理相关视图函数
@login_required
def mail_inbox(request):
    """ 用于查看接收的信息 """
    # update_userInfo_unread_count(request.user)
    inbox_messages = Message.objects.filter(receiver=request.user, 
        msg_type='message', receiver_del=False).order_by('-timestamp')
    context = { 'inbox_messages': inbox_messages }
    return render(request, 'users/mail_inbox.html', context)


@login_required
def mail_outbox(request):
    """ 查看已经发送的消息 """
    outbox_messages = Message.objects.filter(sender=request.user, 
        msg_type='message', sender_del=False).order_by('-timestamp')
    context = { 'outbox_messages': outbox_messages }
    return render(request, 'users/mail_outbox.html', context)


@login_required
def call_admin(request):
    """ 用户发送消息联系管理员 """
    admin_user = User.objects.filter(is_superuser=True)[0]

    if request.method == 'POST':
        response_data = {
            'message': "消息发送失败，请通过邮件联系管理员",
            'next_page': "联系管理员页面",
            'goto_url': settings.CUR_HOST + 'users/call_admin/',
            'goto_time': 5,
        }

        text = request.POST['text']
        if text:
            Message.objects.create(text=text, receiver=admin_user, sender=request.user)
            response_data['message'] = "管理员已经收到消息，将尽快回复"
            response_data['next_page'] = "个人设置页面"
            response_data['goto_url'] = settings.CUR_HOST + 'users/settings'
        
        return render(request, 'users/notice.html' , response_data)

    return render(request, 'users/send_message.html')


@login_required
def send_message(request, user_id):
    try:
        receiver = User.objects.get(id=user_id)
    except ObjectDoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        response_data = {
            'message': "消息内容不可为空",    
            'next_page': "收件箱页面",
            'goto_url': settings.CUR_HOST + 'users/mail_inbox/',
            'goto_time': 2,
        }

        text = request.POST['text']
        if text:
            Message.objects.create(text=text, receiver=receiver, sender=request.user)
            response_data['message'] = "你已回复消息，请等待对方回复"        
        return render(request, 'users/notice.html' , response_data)

    return HttpResponseRedirect(reverse('users:mail_inbox'))


@login_required
def set_as_read(request, message_id):
    """ 标记消息为已读 """
    try:
        message = Message.objects.get(id=message_id)
        if request.user == message.receiver:
            message.is_read = True
            message.save()
    finally:
        return HttpResponseRedirect(reverse('users:mail_inbox'))


@login_required
def read_message(request, message_id):
    """ 阅读消息完整内容并回复 """
    message = Message.objects.get(id=message_id)
    if request.user == message.receiver:
        message.is_read = True
        message.save()

    context = { 'message': message }
    return render(request, 'users/read_message.html', context)


@login_required
def del_message(request, message_id):
    """ 某方删除当前消息，若另一方已删除，则删除该信息 """
    try:
        del_message = Message.objects.get(id=message_id)
    except ObjectDoesNotExist:
        raise Http404

    response = None

    if request.user == del_message.sender:
        del_message.sender_del = True
        if del_message.receiver_del == True:
            del_message.delete()
        else:
            del_message.save()
        response = HttpResponseRedirect(reverse('users:mail_outbox'))

    if request.user == del_message.receiver:
        del_message.receiver_del = True
        del_message.is_read = True
        if del_message.sender_del == True:
            del_message.delete()
        else:
            del_message.save()
        response = HttpResponseRedirect(reverse('users:mail_inbox'))
    
    return response if response != None else HttpResponseRedirect(reverse('users:mail_inbox'))


@login_required
def deal_mult_msg(request):
    msg_ids = request.POST.getlist("checkbox_list")
    if 'delete_msg' in request.POST:
        for idx in msg_ids:
            response = del_message(request, int(idx))
    elif 'set_as_read' in request.POST:
        for idx in msg_ids:
            response = set_as_read(request, int(idx))
    if 'response' in locals().keys():
        return response
    return HttpResponseRedirect(reverse('users:mail_inbox'))