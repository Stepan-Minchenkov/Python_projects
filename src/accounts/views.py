from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from . import models, forms
from django.contrib.auth.models import Group
from bookstore.models import Customer, Book
from reference.models import Author
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404

User = get_user_model()


# Create your views here.
class Homepage(TemplateView):
    template_name = 'main_page.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        top_books = Book.objects.all().order_by('-updated')[:10]
        # top_books = Book.objects.values_list('name', 'price')
        # top_books = Book.objects.filter(
        #     Q(authors__in=Author.objects.filter(Q(name='Agatha') | Q(name='Эдит')))
        # )
        context['object_list'] = top_books
        return context


class Registration(FormView):
    model = User
    form_class = forms.FullUserForm
    template_name = 'accounts/registration.html'

    def form_valid(self, form):
        new_user = form.save()
        new_user.groups.add(Group.objects.get(name='Customers').pk)
        if self.request.user is not None:
            update_session_auth_hash(self.request, self.request.user)
            auth_logout(self.request)
        auth_login(self.request, new_user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:registration_fill')


class RegistrationFill(FormView):
    model = Customer
    form_class = forms.CustomerForm
    template_name = 'accounts/registration_fill.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user
        return context

    def form_valid(self, form):
        form.instance.user_data = self.request.user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homepage')


class ProfileList(ListView):
    model = Customer
    template_name = 'accounts/profile_list.html'


class Profile(DetailView):
    model = User
    template_name = 'accounts/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_groups = []
        for group in context['object'].groups.all():
            user_groups.append(group.name)
        customer_data, created = Customer.objects.get_or_create(user_data=self.request.user.id)
        context['customer_data'] = customer_data
        context['user_groups'] = user_groups
        return context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        userid = request.user.id
        if userid != None:
            self.kwargs["pk"] = userid
        else:
            raise Http404("Error")


class ProfileEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('reference.update_customer', 'reference.update_user')
    model = User
    form_class = forms.ChangeProfileForm
    template_name = 'accounts/profile_edit.html'

    def get_success_url(self):
        customer_data, created = Customer.objects.get_or_create(user_data=self.request.user.id)
        return reverse_lazy('accounts:profile_edit_fill', kwargs={'pk': customer_data.pk})


class ProfileEditFill(PermissionRequiredMixin, UpdateView):
    permission_required = ('reference.update_customer', 'reference.update_user')
    model = Customer
    form_class = forms.ChangeCustomerForm
    template_name = 'accounts/profile_edit_fill.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_name'] = self.request.user
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homepage')
