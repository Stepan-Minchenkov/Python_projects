from django.shortcuts import render
from bookstore.models import Basket
from django.views.generic.edit import FormView
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import models, forms

# Create your views here.


class Orders(generic.ListView):
    model = Basket
    template_name = 'accounts/profile_list.html'


# CRUDl Books:
class ShowBook(generic.ListView):
    #   http://127.0.0.1:8000/bookstore/books
    model = models.Book
    template_name = 'bookstore/book_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'book'
        context['ref_url_update'] = 'bookstore:book-update'
        context['ref_url_delete'] = 'bookstore:book-delete'
        context['ref_url_create'] = 'bookstore:book-create'
        return context


class CreateBook(PermissionRequiredMixin, generic.CreateView):
    #   http://127.0.0.1:8000/bookstore/books-create
    permission_required = 'bookstore.create_books'
    model = models.Book
    form_class = forms.BookForm
    template_name = 'bookstore/book_create.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'book'
        return context


class ReadBook(generic.DetailView):
    #   http://127.0.0.1:8000/bookstore/books/2
    model = models.Book
    template_name = 'bookstore/book_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'book'
        context['ref_type_up'] = 'book'
        context['ref_url'] = 'bookstore:book-show'
        return context


class UpdateBook(PermissionRequiredMixin, generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/books-update/7
    permission_required = 'bookstore.update_books'
    model = models.Book
    form_class = forms.BookForm
    template_name = 'bookstore/book_update.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'book'
        return context


class DeleteBook(PermissionRequiredMixin, generic.DeleteView):
    #   http://127.0.0.1:8000/bookstore/books-delete/7
    permission_required = 'bookstore.delete_books'
    model = models.Book
    template_name = 'bookstore/book_delete.html'
    success_url = reverse_lazy('bookstore:book-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'book'
        context['ref_type_up'] = 'book'
        return context

