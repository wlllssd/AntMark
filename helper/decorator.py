from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import Http404
from django.conf import settings

from users.models import UserInfo

def user_verify_required(func):
    def warpper(*args, **kwargs):
        request = args[0]
        try:
            info = UserInfo.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise Http404

        if info.is_verify == False:
            response_data = {
                'message': "你尚未完成学生认证，暂时无法使用该功能",
                'next_page': "学生认证页面",
                'goto_url': settings.CUR_HOST + 'users/stu_verify',
                'goto_time': 5,
            }
            return render(request, 'users/message.html' , response_data)

        # 执行原来的方法(响应页面)
        response = func(*args, **kwargs)

        return response # 返回内容给前端
    return warpper