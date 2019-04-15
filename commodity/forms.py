from django import forms
from .models import CommodityTag, Commodity

class CommodityTagForm(forms.ModelForm):
    class Meta:
        model = CommodityTag
        fields = ('tag', )


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ('title', 'body', 'price', 'image', 'amount')
