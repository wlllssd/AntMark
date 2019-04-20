from django import forms

from .models import CommodityTag, Commodity, CommoditySource

class CommodityTagForm(forms.ModelForm):
    class Meta:
        model = CommodityTag
        fields = ('tag', )

class CommoditySourceForm(forms.ModelForm):
    class Meta:
        model = CommoditySource
        fields = ('source', )


class CommodityForm(forms.ModelForm):
    class Meta:
        model = Commodity
        fields = ('title', 'body', 'price', 'amount')



