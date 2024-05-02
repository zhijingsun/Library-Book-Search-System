from django.shortcuts import render
# Create your views here.
from django.http import HttpResponse
from login import models
from django.db import connections
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
import logging
from django.contrib.auth import logout
from django.db.utils import OperationalError

logger = logging.getLogger(__name__)

#@login_required(login_url='/admin/adminlogin/')
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if username == 'admin' and password == 'password':
            # 如果验证通过，重定向到查询页面
            #logger.info('User authenticated successfully')
            #print('User authenticated successfully')
            #return render(request, 'admin/execute_query.html')
            return redirect('book_management')
            #return redirect('admin:execute_query')
            #return HttpResponseRedirect(reverse('admin:execute_query'))
        elif username == '' and password == '':
            return redirect('/admin/adminlogin/')
        else: 
            print(username, password)
            # 如果验证失败，返回登录页面并显示错误信息
            #print('User fail')
            error_message = "Invalid username or password. Please try again."
            #logger.warning('User login failed: %s', username) 
            return render(request, 'admin/adminlogin.html', {'error_message': error_message})

    # GET 请求直接显示登录页面
    return render(request, 'admin/adminlogin.html')

def book_management(request):
    books = []
    selected_field = None

    if request.method == 'POST':
        search_term = request.POST.get('search_term', '')
        selected_field = request.POST.get('search_field', '')
        databases = ['book_db0', 'book_db1', 'book_db2']
        
        for database in databases:
            try:
                with connections[database].cursor() as cursor:
                    # 根据选择的字段构造查询语句
                    query = f"SELECT * FROM book WHERE {selected_field} LIKE '%{search_term}%'"
                    cursor.execute(query)
                    rows = cursor.fetchall()
                    books += [{'title': row[2], 'author': row[3], 'isbn': row[1], 'database': database} for row in rows]
            except OperationalError as e:
                error_message = f"Database Error: {str(e)}"
                return render(request, 'admin/error.html', {'error_message': error_message})

    return render(request, 'admin/book_management.html', {'books': books, 'selected_field': selected_field})

def user_management(request):
    users = []
    selected_field = None

    if request.method == 'POST':
        search_term = request.POST.get('search_term', '')
        selected_field = request.POST.get('search_field', '')

        databases = ['user_db0', 'user_db1', 'user_db2']

        for database in databases:
            try:
                with connections[database].cursor() as cursor:
                    # 根据选择的字段构造查询语句
                    query = f"SELECT * FROM users WHERE {selected_field} LIKE '%{search_term}%'"
                    cursor.execute(query)
                    # 获取查询结果
                    rows = cursor.fetchall()
                    # 将查询结果添加到 users 列表中，同时添加数据库标识
                    users += [{'user_name': row[1], 'birthday': row[2], 'email': row[3], 'user_id': row[0], 'password':row[4],'database': database} for row in rows]
            except OperationalError as e:
                error_message = f"Database Error ({database}): {str(e)}"
                return render(request, 'admin/error.html', {'error_message': error_message})

    return render(request, 'admin/user_management.html', {'users': users, 'selected_field': selected_field})

def execute_user_query(request):
    databases = ['user_db0', 'user_db1', 'user_db2']  # 可选的数据库列表

    if request.method == 'POST':
        if 'logout' in request.POST:
            # 如果用户点击了注销按钮
            # logout(request)  # 注销管理员用户
            return redirect('/admin/adminlogin/')

        query = request.POST.get('query', '')
        selected_database = request.POST.get('selected_database', 'user_db0')  # 默认选择第一个数据库

        try:
            with connections[selected_database].cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return render(request, 'admin/result.html', {'result': result, 'query': query})
        except Exception as e:
            return render(request, 'admin/error.html', {'error_message': str(e), 'query': query})

    return render(request, 'admin/execute_user_query.html', {'databases': databases})

#@login_required(login_url='/admin/adminlogin/')
def execute_query(request):
    '''
    if not request.user.is_authenticated:
            return redirect('admin_login')
    '''
    databases = ['book_db0', 'book_db1', 'book_db2']
    if request.method == 'POST':
        if  'logout' in request.POST:
        # 如果用户点击了注销按钮
            # logout(request)  # 注销管理员用户
            return redirect('/admin/adminlogin/')

        query = request.POST.get('query', '')
        print(query)
        selected_database = request.POST.get('selected_database', 'book_db0')
        print(selected_database)
        
        try:
            with connections[selected_database].cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                print(result)
                return render(request, 'admin/result.html', {'result': result})
        except Exception as e:
            return render(request, 'admin/error.html', {'error_message': str(e)})

    return render(request, 'admin/book_management.html')



