from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Product, User

def user_login(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        password = request.POST.get('password')

        password_valid = False
        user = User.objects.get(username='some_username')
        password_valid = user.check_password('raw_password')

        # 使用authenticate函数验证用户
        # user = authenticate(request, user_id=user_id, password=password)

        if user is not None:
            # 用户验证成功，使用login函数登录用户
            password_valid = user.check_password('raw_password')
            login(request, user)
            # 重定向到首页或其他页面
            return redirect('home')  # 假设'home'是首页的URL名称
        else:
            # 用户验证失败，返回登录页面并显示错误消息
            context = {'error': '无效的用户名或密码'}
            return render(request, 'login/login.html', context)
    else:
        # 显示登录表单
        return render(request, 'login/login.html')

def product_list1(request):
    return render(request, 'menu/menu1.html')

def product_list2(request):
    return render(request, 'menu/menu2.html')

def product_list3(request):
    return render(request, 'menu/menu3.html')

def detail(request):
    return render(request, 'other/detail.html')

def product_list3(request):
    return render(request, 'other/payment.html')