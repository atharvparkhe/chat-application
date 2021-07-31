from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.cache import cache
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .threads import *
from .models import Customers

@login_required(login_url='/accounts/login/')
def logoutView(request):
    logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def SignUp(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            password = request.POST.get('password')
            img = request.FILES.get("img")
            try:
                if Customers.objects.filter(email=email).first():
                    messages.info(request, 'This account already exist. Try logging in.')
                    return redirect('/login')
                else:
                    new_customer = Customers.objects.create(email=email, name=name, profile_pic=img)
                    new_customer.set_password(password)
                    new_customer.save()
                    messages.info(request, 'We have sent you a verification OTP.\nPlease check your mail.')
                    return redirect('/verify')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/signup.html")


def Verify(request):
    try:
        if request.method == 'POST':
            otp = request.POST.get('otp')
            try:
                if not cache.get(otp):
                    messages.danger(request, 'Invalid OTP')
                else:
                    customer_obj = Customers.objects.get(email = cache.get(otp))
                    if customer_obj:
                        if customer_obj.is_verified:
                            messages.info(request, 'Your profile is already verified.')
                            return redirect('/login')
                        else :
                            customer_obj.is_verified = True
                            customer_obj.save()
                            messages.success(request, 'Your account has been verified. Please Log In')
                            return redirect('/login')
            except Exception as e:
                print(e)
    except Exception as e :
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/verify.html")


def LogIn(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            try :
                customer_obj = Customers.objects.filter(email=email).first()
                if customer_obj is None:
                    messages.info(request, 'User does not exists. Please Signup')
                    return redirect('/signup')
                if not customer_obj.is_verified:
                    messages.info(request, 'This profile is not verified. Please Check your mail.')
                    return redirect('/login')    
                try:
                    user = authenticate(email=email, password=password)
                    if user is  None:
                        messages.info(request, 'Incorrect Password.')
                        return redirect('/login')
                    login(request, user)
                    messages.info(request, 'Successfully logged in')
                    return redirect('home')
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/login.html")


def Forget(request):
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            if not Customers.objects.get(email=email):
                messages.info(request, 'This user does not exist. Please Signup.')
                return redirect('/signup')
            thread_obj = send_forgot_link(email)
            thread_obj.start()
            messages.info(request, 'We have sent you a link to reset password via mail')
    except Exception as e:
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/forgot.html")


def Reset(request, token):
    try:
        if not cache.get(token):
            messages.info(request, 'The link has expired')
            return redirect('/login')
        else:
            customer_obj = Customers.objects.get(email = cache.get(token))
            if customer_obj:
                try:
                    if request.method == 'POST':
                        npw = request.POST.get('npw')
                        cpw = request.POST.get('cpw')
                        if npw == cpw:
                            customer_obj.set_password(cpw)
                            customer_obj.save()
                            messages.info(request, 'Password Changed successfully.')
                            return redirect('/login')
                except Exception as e:
                    print(e)
            else:
                messages.info(request, 'User does not exist. Please Signup')
                return redirect('/signup')
    except Exception as e :
        print(e)
        messages.info(request, 'Something went Wrong')
    return render(request, "accounts/reset.html")