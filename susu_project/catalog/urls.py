from django.urls import path

from .views import *

urlpatterns = [
    path('books/', BookListView.as_view(), name='books'),
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/<int:book_id>/edit/', BookUpdateView.as_view(), name='book_edit'),
    path('books/<int:book_id>/delete/', BookDeleteView.as_view(), name='book_delete'),

    path('authors/', AuthorListView.as_view(), name='authors'),
    path('authors/add/', AuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:author_id>/edit/', AuthorUpdateView.as_view(), name='author_edit'),
    path('authors/<int:author_id>/delete/', AuthorDeleteView.as_view(), name='author_delete')
]