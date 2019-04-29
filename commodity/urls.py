from django.urls import path, re_path
from . import views

app_name = "commodity"
urlpatterns = [
    path('tag-list/', views.tag_list, name = "tag_list"),
    path('source-list/', views.source_list, name = "source_list"),
    path('commodity-list/', views.commodity_list, name = "commodity_list"),
    path('commodity-detail/<int:commodity_id>/', views.commodity_detail, name = "commodity_detail"),
    path('commodity-repertory/', views.commodity_repertory, name = "commodity_repertory"),
    path('edit-commodity/<int:commodity_id>/', views.edit_commodity, name = "edit_commodity"),
    path('preview-commodity/<int:commodity_id>/', views.preview_commodity, name = "preview_commodity"),
    path('create-commodity/', views.create_commodity, name = "create_commodity"),
    path('del-commodity/', views.del_commodity, name = "del_commodity"),
    path('put-on-shelves-list/', views.put_on_shelves_list, name = "put_on_shelves_list"),
    path('put-off-shelves-list/', views.put_off_shelves_list, name = "put_off_shelves_list"),
    path('put-off-commodity/', views.put_off_commodity, name = "put_off_commodity"),
    path('put-on-commodity/', views.put_on_commodity, name = "put_on_commodity"),
    path('not-verified-list/', views.not_verified_list, name = "not_verified_list"),
    path('commodity-verify/<int:commodity_id>/', views.commodity_verify, name="commodity_verify"),
    path('search-commodity/', views.search_commodity, name = "search_commodity"),
    path('commodity-image/<int:commodity_id>/', views.commodity_image, name = "commodity_image"),
]
