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
    context = {'form': form }
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
            response_data['message'] = e
        
        finally:
            if response_data['success']:
                try:
                    active_code = get_active_code(reg_name)
                    send_active_email(reg_name, active_code)
                except Exception as e:
                    response_data['message'] = '发送激活邮件失败，请稍后重新注册' + str(e)
                    new_user.delete()
                return render(request, 'users/message.html', response_data)
    
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
            Userinfo.objects.create(user=user)
            
 
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

        return render(request, 'users/message.html' , response_data)


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

            return render(request, 'users/message.html' , response_data)

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

def view_notice(request):
    """ 用户查看公告 """
    return render(request, 'home/developing.html')


def call_admin(request):
    """ 用户发送消息联系管理员 """
    return render(request, 'home/developing.html')


@login_required
def stu_verify(request):
    """ 用户提交校园卡照片，后台审核 """
    info = UserInfo.objects.get(user=request.user)
    if info.is_verify:
        response_data = {
            'message': "你已经完成学生认证啦，不用重复认证",
            'next_page': "用户设置页面",
            'goto_url': settings.CUR_HOST + 'users/settings/', 
            'goto_time': 5,
        }
        return render(request, 'users/message.html' , response_data)

    if request.method == 'POST':
        stu_card_photo = request.FILES.get('stu_card_photo', None)
        if stu_card_photo:
            info.stuCardPhoto = stu_card_photo
        info.save()
        return HttpResponseRedirect(reverse('users:settings'))

    return render(request, 'users/student_verify.html')



