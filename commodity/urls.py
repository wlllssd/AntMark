from django.urls import path, re_path
from . import views

app_name = "commodity"
urlpatterns = [
    path('tag-list/', views.tag_list, name = "tag_list"),
    path('source-list/', views.source_list, name = "source_list"),
    path('commodity-list/', views.commodity_list, name = "commodity_list"),
    path('commodity-detail/<int:id>/', views.commodity_detail, name = "commodity_detail"),
    path('commodity-repertory/', views.commodity_repertory, name = "commodity_repertory"),
    path('edit-commodity/<int:id>/', views.edit_commodity, name = "edit_commodity"),
    path('create-commodity/', views.create_commodity, name = "create_commodity"),
    path('del-commodity/', views.del_commodity, name = "del_commodity"),
    path('put-on-shelves_list/', views.put_on_shelves_list, name = "put_on_shelves_list"),
    path('put-off-shelves_list/', views.put_off_shelves_list, name = "put_off_shelves_list"),
    path('put-off-commodity/', views.put_off_commodity, name = "put_off_commodity"),
    path('put-on-commodity/', views.put_on_commodity, name = "put_on_commodity"),
    # path('search_commodity/', views.search_commodity, name = "search_commodity"),
    # re_path('search-commodity/filter', views.commodity_filter, name = "commodity_filter"),
    path('search_commodity/', views.search_and_filter_commodity, name = "search_and_filter_commodity")
]
