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
    path('authors/<int:author_id>/delete/', AuthorDeleteView.as_view(), name='author_delete'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    path('register/check_login', check_login_view, name='check_login'),
    path('profile/', ProfileView.as_view(), name='profile'),

    path('cart/', CartDetailView.as_view(), name='cart_detail'),
    path('cart/add/<int:book_id>', CartAddView.as_view(), name='cart_add'),
    path('cart/delete/<int:book_id>', CartDeleteView.as_view(), name='cart_delete'),
]
