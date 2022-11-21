from django.urls import path

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views as bookstore_views

app_name = 'bookstore'
urlpatterns = [
    path('orders/', bookstore_views.Orders.as_view(), name='orders'),

    path('books/<int:pk>', bookstore_views.ReadBook.as_view(), name='book-detail'),
    path('books/', bookstore_views.ShowBook.as_view(), name='book-show'),
    path('books-create/', bookstore_views.CreateBook.as_view(), name='book-create'),
    path('books-delete/<int:pk>', bookstore_views.DeleteBook.as_view(), name='book-delete'),
    path('books-update/<int:pk>', bookstore_views.UpdateBook.as_view(), name='book-update'),
]
