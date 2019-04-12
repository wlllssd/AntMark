from django.urls import path
from . import views

app_name = "commodity"
urlpatterns = [
    path('tag-list/', views.tag_list, name = "tag_list"),
    path('commodity-list/', views.commodity_list, name = "commodity_list"),
    path('commodity-detail/<int:id>/', views.commodity_detail, name = "commodity_detail"),
]



# from django.urls import path
# from . import views


# app_name = 'news'
# urlpatterns = [
# 	path('', views.news_title, name= 'news_title'),
# 	path('<int:article_id>', views.news_article, name= 'news_article'),
# ]