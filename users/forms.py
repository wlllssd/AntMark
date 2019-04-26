from django import forms
#from markdown import MarkdownFormField
from users.models import UserInfo


#class ProfileForm(forms.Form):
 #   upProfile = forms.FileField()

class InfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            'nickname',
            'gender',
            'intro',
            'phone',
            'wechat',
            'qq',
        ]
        labels = {
            'nickname': '昵称',
            'gender': '性别',
            'intro': '个人简介',
            'phone': '电话',
            'wechat': '微信',
            'qq': 'QQ',
        }