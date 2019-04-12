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
        
        ]
        labels = {
            'nickname': 'Nickname',
            'gender': 'Gender',
            'intro': 'User introduce',
        }