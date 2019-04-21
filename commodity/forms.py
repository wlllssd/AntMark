from django import forms
from DjangoUeditor.models import UEditorField

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

class UEditorForm(forms.Form):
    body = UEditorField(verbose_name = "commodity_descriprion",imagePath="ueditorImages/", 
		width=700, height=600, filePath='ueditorFiles/', toolbars="full")


