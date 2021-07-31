from django.shortcuts import render

def homePage(request):
    print(request.user)
    return render(request, "main/home.html")