from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password, check_password
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *
from .auth import *


class FormException(Exception):
    pass


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        try:
            if not form.is_valid():
                raise FormException("Форма не действительна.")

            data = form.cleaned_data

            try:
                user = User.objects.get(login=data['login'])
            except:
                user = None

            if user is None:
                raise FormException("Пользователь не найден.")

            if not check_password(data['password'], user.password):
                raise FormException("Неверный пароль.")

            request.session['user_id'] = user.pk
            return HttpResponseRedirect(reverse_lazy('books'))

        except FormException as e:
            msg, = e.args
            form.add_error(None, msg)

    else:
        form = LoginForm()

    return render(request, 'catalog/auth/login_form.html', {
        'form': form
    })


def logout_view(request):
    request.session.flush()
    return HttpResponseRedirect(reverse_lazy('login'))


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)

        try:
            if not form.is_valid():
                raise FormException('Форма не действительна.')

            data = form.cleaned_data

            try:
                user = User.objects.get(login=data['login'])
            except:
                user = None

            if user is not None:
                raise FormException('Пользователь с с таким логином уже существует.')

            try:
                user = User.objects.get(email=data['email'])
            except:
                user = None

            if user is not None:
                raise FormException('Пользователь с такой электропочтой уже существует.')

            user = User.objects.create(
                login=data['login'],
                email=data['email'],
                name=data['name'],
                password=make_password(data['password'], None, 'md5'),
                role='USR'
            )
            request.session['user_id'] = user.pk
            return HttpResponseRedirect(reverse_lazy('books'))

        except FormException as e:
            msg, = e.args
            form.add_error(None, msg)

    else:
        form = RegisterForm()

    return render(request, 'catalog/auth/register_form.html', {
        'form': form
    })


class BookListView(AuthMixin, ListView):
    paginate_by = 5
    model = Book
    template_name = 'catalog/book_table.html'
    context_object_name = 'books'


class AuthorListView(AuthMixin, ListView):
    paginate_by = 5
    model = Author
    template_name = 'catalog/author_table.html'
    context_object_name = 'authors'


class BookCreateView(AuthMixin, CreateView):
    form_class = BookForm
    template_name = 'catalog/book_form.html'
    extra_context = {'is_edit_mode': False}
    success_url = reverse_lazy('books')
    required_perms = ['BOOKS_CREATE']
    forbidden_url = reverse_lazy('books')


class AuthorCreateView(AuthMixin, CreateView):
    form_class = AuthorForm
    template_name = 'catalog/author_form.html'
    extra_context = {'is_edit_mode': False}
    success_url = reverse_lazy('authors')
    required_perms = ['AUTHORS_CREATE']
    forbidden_url = reverse_lazy('authors')


class BookUpdateView(AuthMixin, UpdateView):
    model = Book
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'
    form_class = BookForm
    template_name = 'catalog/book_form.html'
    extra_context = {'is_edit_mode': True}
    success_url = reverse_lazy('books')
    required_perms = ['BOOKS_UPDATE']
    forbidden_url = reverse_lazy('books')


class AuthorUpdateView(AuthMixin, UpdateView):
    model = Author
    pk_url_kwarg = 'author_id'
    context_object_name = 'author'
    form_class = AuthorForm
    template_name = 'catalog/author_form.html'
    extra_context = {'is_edit_mode': True}
    success_url = reverse_lazy('authors')
    required_perms = ['AUTHORS_UPDATE']
    forbidden_url = reverse_lazy('authors')


class BookDeleteView(AuthMixin, DeleteView):
    model = Book
    pk_url_kwarg = 'book_id'
    success_url = reverse_lazy('books')
    required_perms = ['BOOKS_DELETE']
    forbidden_url = reverse_lazy('books')


class AuthorDeleteView(AuthMixin, DeleteView):
    model = Author
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy('authors')
    required_perms = ['AUTHORS_DELETE']
    forbidden_url = reverse_lazy('authors')
