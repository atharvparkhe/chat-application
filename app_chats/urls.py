from django.urls import path
from . import views
from .views import *

urlpatterns = [
	path('chat/<room_id>/', views.chatPage, name="chat"),
	# path('show-chat/<room_id>/', views.showPreviousChats, name="show-chat"),
]