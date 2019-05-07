from django.urls import path

from admin_manage import views

app_name = 'admin_manage'

urlpatterns = [
    path('', views.admin_index, name = 'admin_index'),
    
    path('stu_verify_list', views.stu_verify_list, name = "stu_verify_list"),
    
    path('comm_verify_list', views.comm_verify_list, name = "comm_verify_list"),
    
    path('stu_verify_detail/<int:message_id>/<int:user_id>', views.stu_verify_detail, name = "stu_verify_detail"),

    path('comm_verify_detail/<int:message_id>/<int:comm_id>', views.comm_verify_detail, name = "comm_verify_detail"),

    path('create_anno/', views.create_anno, name = "create_anno"),

    path('read_message/<int:message_id>', views.read_message, name = 'read_message'),

    path('del_message/<int:message_id>', views.del_message, name = 'del_message'),

    path('deal_mult_msg/', views.deal_mult_msg, name = 'deal_mult_msg'),
]
