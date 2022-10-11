from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *


class BookListView(ListView):
    paginate_by = 5
    model = Book
    template_name = 'catalog/book_table.html'
    context_object_name = 'books'


class AuthorListView(ListView):
    paginate_by = 5
    model = Author
    template_name = 'catalog/author_table.html'
    context_object_name = 'authors'


class BookCreateView(CreateView):
    form_class = BookForm
    template_name = 'catalog/book_form.html'
    extra_context = {'is_edit_mode': False}
    success_url = reverse_lazy('books')


class AuthorCreateView(CreateView):
    form_class = AuthorForm
    template_name = 'catalog/author_form.html'
    extra_context = {'is_edit_mode': False}
    success_url = reverse_lazy('authors')


class BookUpdateView(UpdateView):
    model = Book
    pk_url_kwarg = 'book_id'
    context_object_name = 'book'
    form_class = BookForm
    template_name = 'catalog/book_form.html'
    extra_context = {'is_edit_mode': True}
    success_url = reverse_lazy('books')


class AuthorUpdateView(UpdateView):
    model = Author
    pk_url_kwarg = 'author_id'
    context_object_name = 'author'
    form_class = AuthorForm
    template_name = 'catalog/author_form.html'
    extra_context = {'is_edit_mode': True}
    success_url = reverse_lazy('authors')


class BookDeleteView(DeleteView):
    model = Book
    pk_url_kwarg = 'book_id'
    success_url = reverse_lazy('books')


class AuthorDeleteView(DeleteView):
    model = Author
    pk_url_kwarg = 'author_id'
    success_url = reverse_lazy('authors')