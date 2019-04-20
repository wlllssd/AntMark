from django.urls import path

from chatroom import views

app_name = 'chatroom'

urlpatterns = [
    # 聊天室列表
    path('room_list/', views.room_list, name = 'room_list'),

    path('start_chat/<int:user_id>/<int:comm_id>', views.start_chat, name = 'start_chat'),

    path('room_detail/<int:room_id>', views.room_detail, name = 'room_detail'),

    path('get_messages/<int:room_id>', views.get_messages, name = 'get_messages'),
]
