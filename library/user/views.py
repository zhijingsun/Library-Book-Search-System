from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from contextlib import nullcontext
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db import connections
from .forms import BookSearchForm, AddToListForm
from django.db.models import Q
from login import models
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    user_id = request.GET.get('user_id', None)
    user_name = 'Guest'

    if user_id:
        db_index = int(user_id) % 3
        database = f'user_db{db_index}'

        user = get_object_or_404(models.User.objects.using(database), pk=user_id)
        user_name = user.user_name

    form = BookSearchForm(request.GET)
    books = []

    if form.is_valid():
        query = form.cleaned_data.get('search_query')
        search_type = form.cleaned_data.get('search_type')
        start_year = form.cleaned_data.get('start_year')
        end_year = form.cleaned_data.get('end_year')
        order_by = form.cleaned_data.get('order_by')
        if not order_by or order_by not in ['title', 'author', 'publication_year']:
            order_by = 'title'
        order_direction = form.cleaned_data.get('order_direction')

        q_objects = Q()
        if query:
            if search_type == 'title':
                q_objects |= Q(title__icontains=query)
            elif search_type == 'author':
                q_objects |= Q(author__icontains=query)
            elif search_type == 'isbn':
                q_objects |= Q(isbn__icontains=query)
            else:
                q_objects |= Q(title__icontains=query) | Q(author__icontains=query) | Q(isbn__icontains=query)

        if start_year and end_year:
            q_objects &= Q(publication_year__range=(start_year, end_year))

        all_books = []
        databases = ['book_db0', 'book_db1', 'book_db2']
        for db in databases:
            all_books += list(models.Book.objects.using(db).filter(q_objects))

        if order_direction == 'desc':
            order_by = '-' + order_by
        books = sorted(all_books, key=lambda x: getattr(x, order_by.strip('-')), reverse=(order_direction == 'desc'))

    return render(request, 'user/templates/index.html', {'user_id': user_id, 'user_name': user_name, 'form': form, 'books': books})

def book_detail(request, book_id):
    db_index = book_id % 3
    database = f'book_db{db_index}'
    book = get_object_or_404(models.Book.objects.using(database), pk=book_id)
    return render(request, 'book_detail.html', {'book': book})

def mylist(request, user_id):
    db_index = int(user_id) % 3
    database = f'user_db{db_index}'
    user = get_object_or_404(models.User.objects.using(database), pk=user_id)

    if request.method == 'POST':
        if 'delete' in request.POST:
            book_id = request.POST.get('book_id')
            with connections[database].cursor() as cursor:
                cursor.execute("DELETE FROM favorite WHERE user_id = %s AND book_id = %s", [user_id, book_id])
            # models.Favorite.objects.using(database).filter(user_id=user_id, book_id=book_id).delete()
            messages.success(request, 'Book removed successfully!')
            return redirect('mylist', user_id=user_id)

    with connections[database].cursor() as cursor:
        cursor.execute("SELECT book_id FROM favorite WHERE user_id = %s", [user_id])
        favorites = cursor.fetchall()
    books = []
    if favorites:
        for favorite in favorites:
            db_index = favorite[0] % 3
            book_db = f'book_db{db_index}'
            book = models.Book.objects.using(book_db).get(pk=favorite[0])
            books.append(book)
    return render(request, 'mylist.html', {'user': user, 'books': books})


def add_to_list(request):
    user_id = request.POST.get('user_id', None)
    if user_id is not None and request.method == 'POST':
        form = AddToListForm(request.POST)
        if form.is_valid():
            book_id = form.cleaned_data['book_id']
            print(1)
            db_index = int(user_id) % 3
            database = f'user_db{db_index}'
            if models.Favorite.objects.using(database).filter(user_id=user_id, book_id=book_id).exists():
                messages.error(request, 'This book is already added to your list.')
            else:
                models.Favorite.objects.using(database).create(user_id=user_id, book_id=book_id)
                messages.success(request, 'Book added successfully.')
        return redirect('/user/index?user_id={}'.format(user_id))

    return redirect('/user/index?user_id={}'.format(user_id))


def profile(request, user_id):
    db_index = int(user_id) % 3
    database = f'user_db{db_index}'
    user = get_object_or_404(models.User.objects.using(database), pk=user_id)
    return render(request, 'profile.html', {'user': user})


def edit_profile(request, user_id):
    db_index = int(user_id) % 3
    database = f'user_db{db_index}'
    user = get_object_or_404(models.User.objects.using(database), pk=user_id)
    if request.method == 'POST':
        user_name = request.POST.get('username')
        birthday = request.POST.get('birthday')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'profile.html', {'user': user})

        user.user_name = user_name
        user.birthday = birthday
        user.email = email
        if password:
            user.password = make_password(password)

        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile', user_id=user_id)
    else:
        return render(request, 'profile.html', {'user': user})


def change_password(request, user_id):
    db_index = int(user_id) % 3
    database = f'user_db{db_index}'
    user = get_object_or_404(models.User.objects.using(database), pk=user_id)

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if old_password != user.password:
            print(old_password, user.password)
            messages.error(request, "Your old password was entered incorrectly. Please enter it again.")
            return redirect('profile', user_id=user_id)

        if new_password and new_password != confirm_new_password:
            messages.error(request, "The two password fields didn't match.")
            return redirect('profile', user_id=user_id)

        user.password = new_password
        user.save()

        messages.success(request, "Your password was successfully updated!")
        return redirect('profile', user_id=user_id)

    return redirect('profile', user_id=user_id)

def delete_user(request, user_id):
    db_index = int(user_id) % 3
    database = f'user_db{db_index}'
    user = get_object_or_404(models.User.objects.using(database), pk=user_id)

    if request.method == 'POST':
        user.delete()
        return redirect('/login/login/')

    return redirect("/login/login/")

def logout(request):
    pass
    return redirect("/login/login/")
