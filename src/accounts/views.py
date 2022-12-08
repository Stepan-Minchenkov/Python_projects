from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic import ListView, DetailView, UpdateView, TemplateView
from . import forms
from django.contrib.auth.models import Group
from bookstore.models import Customer, Book
from django.db.models import Q
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.conf import settings

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


# def url(request):
#     return HttpResponseRedirect(settings.NBRBBY)
#

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
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        object_list = None
        current_user = User.objects.filter(username=self.request.user)
        if current_user:
            current_user = User.objects.get(username=self.request.user)
            object_list = \
                Customer.objects.filter(
                    Q(user_data__in=User.objects.filter(
                        Q(groups__name="Customers") &
                        ~Q(username=current_user))
                      ))
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        return context


class ProfileListCustomers(ListView):
    model = Customer
    template_name = 'accounts/profile_list_customers.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        object_list = User.objects.filter(Q(groups__name="Customers"))
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        return context


class ProfileListManagers(ListView):
    model = Customer
    template_name = 'accounts/profile_list_managers.html'
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        object_list = User.objects.filter(Q(groups__name="Managers"))
        context = super().get_context_data(*args, object_list=object_list, **kwargs)
        return context


class Profile(DetailView):
    model = User
    template_name = 'accounts/profile_read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        Customer.objects.get_or_create(
            user_data=user,
            defaults={
                'phone': '',
                'country': '',
                'city': '',
                'zip_code': '',
                'address1': '',
                'address2': ''
            }
        )
        return context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        if self.kwargs.get("pk") is None:
            userid = request.user.id
            if userid is not None:
                self.kwargs["pk"] = userid
            else:
                raise Http404("Error")


class ProfileEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('bookstore.change_customer', 'auth.change_user')
    model = User
    form_class = forms.ChangeProfileForm
    template_name = 'accounts/profile_edit.html'

    def get(self, request, *args, **kwargs):
        get_object = super().get(self, request, *args, **kwargs)
        if self.request.user.pk != self.object.pk:
            raise PermissionDenied()
        return get_object

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # user = User.objects.get(username=self.request.user)
        # customer, created = Customer.objects.get_or_create(
        #     user_data=user,
        #     defaults={
        #         'phone': '',
        #         'country': '',
        #         'city': '',
        #         'zip_code': '',
        #         'address1': '',
        #         'address2': ''
        #     }
        # )
        # object_temp = context.get('object')
        # del context['form']
        # # context['form'] = forms.ChangeProfileForm(data={
        # #     'email': object_temp.email,
        # #     'first_name': object_temp.first_name,
        # #     'last_name': object_temp.last_name,
        # #     'phone': customer.phone,
        # # })
        # context['form'] = forms.ChangeProfileForm(instance=object_temp)
        return context

    def form_valid(self, form):
        customer = Customer.objects.get(user_data=self.request.user)
        # customer.phone = form.cleaned_data['phone']
        customer.phone = form['phone'].value()
        customer.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('accounts:profile')
