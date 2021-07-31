from django.shortcuts import render
from .models import *
from app_accounts.models import Customers
from django.http import JsonResponse

def chatPage(request, room_id):
    context = {}
    try:
        print(request.user)
        user = Customers.objects.get(email = request.user)
        room = Room.objects.get(id = room_id)
        context["user"] = user
        context["room"] = room
        for i in room.members.all():
            if i.email != user.email:
                context["chatting_to"] = i
            else:
                pass

    except Exception as e:
        print(e)
    return render(request, "chat/chat.html", context)

# def showPreviousChats(room_id):
#     result = {'message' : 'something went wrong' , 'status' : False}
#     try:
#         room_obj = Room.objects.get(id = room_id)
#         chats_objs = Chat.objects.get(group = room_obj)
#         result['message'] = 'This are the messages.'
#         result['data'] = {'chats_objs' : chats_objs}
#         result['status'] = True
#     except Exception as e:
#         print(e)
#     return JsonResponse({"result":result})