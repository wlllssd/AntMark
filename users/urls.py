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

    path('reset_pwd/', views.reset_password, name = 'reset_pwd'),

    path('view_notice/', views.view_notice, name = 'view_notice'),

    path('call_admin/', views.call_admin, name = 'call_admin'),

    # 聊天室列表
    path('notice/', views.notice, name = 'notice'),

    path('start_chat/<int:user_id>', views.start_chat, name = 'start_chat'),

    path('chatting/<int:room_id>', views.chatting, name = 'chatting'),

]

