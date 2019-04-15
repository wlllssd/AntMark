from django.contrib import admin
from .models import Commodity, CommodityTag, CommoditySource

class CommodityTagAdmin(admin.ModelAdmin):
    list_display = ('tag',)
admin.site.register(CommodityTag, CommodityTagAdmin)

class CommodityAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'amount','for_sale', 'created')
admin.site.register(Commodity, CommodityAdmin)

class CommoditySourceAdmin(admin.ModelAdmin):
    list_display = ('source', )
admin.site.register(CommoditySource, CommoditySourceAdmin)
