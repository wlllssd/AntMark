from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.hashers import make_password, check_password
from django.template import Context, loader 

from helper.crypto import encrypt, decrypt
from django.conf import settings

import re, time

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
            pattern = re.compile('^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')
            match = pattern.match(reg_name)
            if not match:
                raise Exception('邮箱格式错误')

            pattern = re.compile('^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,16}$')
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
    key, context = 9, {}
    try:
        decrypt_str = decrypt(key,active_code)
        decrypt_data = decrypt_str.split('|')
        email = decrypt_data[0]                                   #邮箱
        create_date = time.strptime(decrypt_data[1], "%Y-%m-%d")  #激活链接创建日期
        create_date = time.mktime(create_date)            #struct_time 转成浮点型的时间戳
 
        day = int((time.time()-create_date)/(24*60*60))     #得到日期差
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
 
        context['goto_page'] = True
        context['message'] = '激活成功，欢迎加入AntMark！'

    except IndexError as e:
        context['goto_page'] = False
        context['message'] = '激活链接无效'
    
    except Exception as e:
        context['goto_page'] = False
        context['message'] = e
    
    finally:
        #激活成功就跳转到首页(message页面有自动跳转功能)
        context['goto_url'] = settings.CUR_HOST
        context['goto_time'] = 3000

        return render(request, 'users/message.html' , context)

def user_settings(request):
    pass