from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect
from . import models
from . import forms
from .models import User
from django.db import transaction

# def index(request):
#     pass
#     return render(request, 'login/templates/index.html')


def login(request):
    if request.method == 'POST':
        login_form = forms.UserForm(request.POST)
        print(login_form)
        message = 'Please check the contents!'
        if login_form.is_valid():
            email = login_form.cleaned_data.get('email')
            password = login_form.cleaned_data.get('password')
            
            databases = ['user_db0', 'user_db1', 'user_db2']
            for db in databases:
                try:
                    user = models.User.objects.using(db).get(email=email)
                except models.User.DoesNotExist:
                    continue  # 如果用户不存在于当前数据库，则继续尝试下一个数据库
                if user.password == password:
                    user_id = user.user_id
                    return redirect('/user/index/?user_id={}'.format(user_id))
                else:
                    message = 'The password is incorrect!'
                    print(user.password, email, password)
                    return render(request, 'login/templates/login.html', locals())
            
            # 如果遍历完所有数据库仍未找到用户，则返回用户不存在消息
            message = 'The user does not exist!'
            return render(request, 'login/templates/login.html', locals())
        else:
            return render(request, 'login/templates/login.html', locals())

    login_form = forms.UserForm()
    return render(request, 'login/templates/login.html', locals())




def signup(request):
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "Please check the content!"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            birthday = register_form.cleaned_data.get('birthday')
            email = register_form.cleaned_data.get('email')
            password = register_form.cleaned_data.get('password')
            confirm_password = register_form.cleaned_data.get('confirm_password')

            if password != confirm_password:
                message = 'Re-entered password is different!'
                print(password, confirm_password)
                return render(request, 'login/templates/signup.html', locals())

            # 检查是否已经存在相同邮箱的用户
            for db in ['user_db0', 'user_db1', 'user_db2']:
                try:
                    user = models.User.objects.using(db).get(email=email)
                    message = 'This email has already been registered!'
                    print(user)
                    return render(request, 'login/templates/signup.html', locals())
                except models.User.DoesNotExist:
                    continue

            # 创建新用户并保存到相应的数据库
            new_user = models.User(user_name=username, 
                                   birthday=birthday,
                                   email=email, 
                                   password=password)
            print(1)
            new_user.save()
            print(2)
            # 获取新用户的 ID
            user_id = new_user.user_id
            print(3)

            # 根据用户 ID 的取余选择数据库
            db_index = user_id % 3
            db_name = f'user_db{db_index}'

            with transaction.atomic(using=db_name):
                new_user.save(using=db_name)
            
            # 从 'total' 数据库中删除用户数据
            models.User.objects.filter(email=email).delete()

            return redirect('/login/login/')
        else:
            return render(request, 'login/templates/signup.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'login/templates/signup.html', locals())


# def logout(request):
#     pass
#     return redirect("/login/")