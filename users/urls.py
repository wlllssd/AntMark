from django.urls import path

from users import views
app_name = 'users'

urlpatterns = [
    # 基础功能
    path('login/', views.login_view, name = 'login'),

    path('logout/', views.logout_view, name = 'logout'),

    path('register/', views.user_reg, name = 'register'),

    path('active/<str:active_code>', views.user_active, name = 'active'),

    path('settings/', views.user_settings, name = 'settings'),

    # path('notice/', views.notice, name = 'notice'),

    # path('reset_password/', views.reset_password, name = 'reset_password'),

	# path('reset_done/', views.reset_done, name = 'reset_done'),

    
]

