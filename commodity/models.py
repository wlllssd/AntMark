from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from DjangoUeditor.models import UEditorField
# from ckeditor.fields import RichTextField
# from ckeditor_uploader.fields import RichTextUploadingField

# 商品标签
class CommodityTag(models.Model):
	tag = models.CharField(max_length = 300)

	def __str__(self):
		return self.tag

# 商品货源
class CommoditySource(models.Model):
	source = models.CharField(max_length = 300)
	
	def __str__(self):
		return self.source

# 商品
class Commodity(models.Model):
	title = models.CharField(max_length = 300)
	owner = models.ForeignKey(User, related_name = "commodity", on_delete = models.CASCADE)
	commodity_tag = models.ManyToManyField(CommodityTag, related_name = "commodity_tag", blank = False)
	commodity_source = models.ManyToManyField(CommoditySource, related_name = "commodity_source", blank = False)
	body = UEditorField(verbose_name = "commodity_descriprion",imagePath="ueditorImages/", 
			width=700, height=600, filePath='ueditorFiles/', toolbars="full")
	price = models.DecimalField(max_digits=7, decimal_places=2, default = 0.00)
	image = models.ImageField(upload_to = 'images/%Y/%m/%d')
	amount = models.IntegerField(default = 1)
	for_sale = models.BooleanField(default = True)
	created = models.DateTimeField(default = timezone.now)
	updated = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ('-updated',)

	def __str__(self):
		return self.title