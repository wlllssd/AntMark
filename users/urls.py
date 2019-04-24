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

    path('personal_index/<int:user_id>', views.personal_index, name = 'personal_index'),

    path('stu_verify/', views.stu_verify, name = 'stu_verify'),

    
    # 消息处理相关
    path('mail_inbox/', views.mail_inbox, name = 'mail_inbox'),

    path('mail_outbox/', views.mail_outbox, name = 'mail_outbox'),

    path('call_admin/', views.call_admin, name = 'call_admin'),

    path('set_as_read/<int:message_id>', views.set_as_read, name = 'set_as_read'),

    path('read_message/<int:message_id>', views.read_message, name = 'read_message'),

    path('del_message/<int:message_id>', views.del_message, name = 'del_message'),

    path('deal_mult_msg/', views.deal_mult_msg, name = 'deal_mult_msg'),

]