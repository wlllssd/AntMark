from django.contrib import admin
from .models import Commodity, CommodityTag

class CommodityTagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
admin.site.register(CommodityTag, CommodityTagAdmin)

class CommodityAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created')
admin.site.register(Commodity, CommodityAdmin)
