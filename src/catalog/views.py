import re

from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.decorators.http import require_POST
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .auth import *
from .cart import Cart
from .forms import *
from .models import *


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
                raise FormException('Пользователь с таким логином уже существует.')

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
                role='CST'
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


@require_POST
def check_login_view(request):
    user_login = request.POST.get('user_login')

    try:
        User.objects.get(login=user_login)
        return JsonResponse({'status': 'taken'})
    except:
        return JsonResponse({'status': 'free'})


class BookListView(AuthMixin, ListView):
    paginate_by = 5
    template_name = 'catalog/book_table.html'
    context_object_name = 'books'
    required_perms = ['BOOKS_READ']
    forbidden_url = reverse_lazy('login')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['cart_book_form'] = CartAddBookForm()
        context['cart'] = Cart(self.request)
        context['book_list_page'] = True

        book_query = self.request.GET.get('book_query')
        if book_query:
            context['book_query'] = book_query

        return context

    def get(self, request, *args, **kwargs):
        book_query = self.request.GET.get('book_query')

        if book_query:
            self.queryset = Book.objects.filter(title__icontains=book_query)
        else:
            self.model = Book

        return super().get(request, *args, **kwargs)


class AuthorListView(AuthMixin, ListView):
    paginate_by = 5
    model = Author
    template_name = 'catalog/author_table.html'
    context_object_name = 'authors'
    required_perms = ['AUTHORS_READ']
    forbidden_url = reverse_lazy('books')


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


class ProfileView(AuthMixin, UpdateView):
    model = User
    context_object_name = 'user'
    form_class = ProfileForm
    template_name = 'catalog/profile_form.html'
    success_url = reverse_lazy('books')
    required_perms = ['PROFILE']
    forbidden_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.auth.user


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


class CartAddView(AuthMixin, View):
    required_perms = ['BOOKS_SHOP']
    forbidden_url = reverse_lazy('login')

    def post(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        form = CartAddBookForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(
                book=book,
                quantity=cd['quantity'],
                update_quantity=cd['update']
            )
        return redirect('cart_detail')


class CartDeleteView(AuthMixin, View):
    required_perms = ['BOOKS_SHOP']
    forbidden_url = reverse_lazy('login')

    def get(self, request, book_id):
        cart = Cart(request)
        book = get_object_or_404(Book, id=book_id)
        cart.delete(book)
        return redirect('cart_detail')


class CartDetailView(AuthMixin, View):
    required_perms = ['BOOKS_SHOP']
    forbidden_url = reverse_lazy('login')

    def get(self, request):
        cart = Cart(request)
        return render(request, 'catalog/cart/cart_detail.html', {
            'cart': cart,
            **self.get_context_data()
        })
