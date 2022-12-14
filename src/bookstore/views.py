from django.shortcuts import render
from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import models, forms
from django.db.models import Q
from django.core.exceptions import PermissionDenied, ValidationError, NON_FIELD_ERRORS
from reference.models import Author, Serie, Publisher, Genre
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.utils.translation import gettext_lazy as _
from django.forms.utils import ErrorList

User = get_user_model()


# Create your views here.
# CRUDl Books:
class ShowBook(generic.ListView):
    #   http://127.0.0.1:8000/bookstore/books
    model = models.Book
    template_name = 'bookstore/book_list.html'
    paginate_by = 4

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class CreateBook(PermissionRequiredMixin, generic.CreateView):
    #   http://127.0.0.1:8000/bookstore/books-create
    permission_required = 'bookstore.add_book'
    model = models.Book
    form_class = forms.BookForm
    template_name = 'bookstore/book_create.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class ReadBook(generic.DetailView):
    #   http://127.0.0.1:8000/bookstore/books/2
    model = models.Book
    template_name = 'bookstore/book_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class UpdateBook(PermissionRequiredMixin, generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/books-update/7
    permission_required = 'bookstore.change_book'
    model = models.Book
    form_class = forms.BookForm
    template_name = 'bookstore/book_update.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class DeleteBook(PermissionRequiredMixin, generic.DeleteView):
    #   http://127.0.0.1:8000/bookstore/books-delete/7
    permission_required = 'bookstore.delete_book'
    model = models.Book
    template_name = 'bookstore/book_delete.html'
    success_url = reverse_lazy('bookstore:book-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


# CRUDl Basket:
class ShowBasket(generic.ListView):
    #   http://127.0.0.1:8000/bookstore/orders
    model = models.Basket
    template_name = 'bookstore/orders_list.html'
    paginate_by = 5

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_queryset(self):
        basket = ''

        if self.request.user.is_authenticated:
            if self.request.user.has_perm("auth.manager") or \
                    self.request.user.has_perm("auth.admin"):
                basket = models.Basket.objects.all().order_by("order_status", "-pk")
            elif self.request.user.has_perm("auth.registered_customer"):
                customer = self.request.user
                basket = models.Basket.objects.filter(customer=customer).order_by("order_status", "-pk")
        return basket


class ReadBasket(generic.DetailView):
    #   http://127.0.0.1:8000/bookstore/orders/2
    model = models.Basket
    template_name = 'bookstore/orders_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class UpdateBasket(PermissionRequiredMixin, generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/orders-update/7
    permission_required = 'bookstore.change_basket'
    model = models.Basket
    form_class = forms.BasketForm
    template_name = 'bookstore/orders_update.html'

    def get(self, request, *args, **kwargs):
        get_object = super().get(self, request, *args, **kwargs)
        if not self.request.user.is_authenticated:
            if request.session['basket_pk'] != self.object.pk:
                raise PermissionDenied()

        if not self.request.user.has_perm("auth.manager") and \
                not self.request.user.has_perm("auth.admin"):
            customer = self.request.user
            baskets = models.Basket.objects.filter(customer=customer)
            customer_basket = False
            for basket in baskets:
                if basket.pk == self.object.pk:
                    customer_basket = True
                    break

            if not customer_basket:
                raise PermissionDenied()
        return get_object

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        del self.request.session['update_basket_id']
        return reverse_lazy('bookstore:orders-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.request.session['update_basket_id'] = self.object.pk
        return context

    def form_valid(self, form):
        if self.request.user.has_perm("auth.manager") or \
                self.request.user.has_perm("auth.admin"):
            basket = models.Basket.objects.get(pk=form.instance.pk)
            if basket.order_status == "created" and \
                    form.instance.order_status == "in_process":
                goods_in_basket = models.GoodsInBasket.objects.filter(order=form.instance.pk)
                for goods in goods_in_basket:
                    book = models.Book.objects.get(pk=goods.article.pk)
                    book.available -= goods.quantity
                    if book.available < 0:
                        message = f"Request has more book '{book.name}' than there are available. Please decrease."
                        form._errors[NON_FIELD_ERRORS] = ErrorList([
                            message
                        ])
                        return self.form_invalid(form)
                        # raise ValidationError(
                        #     _("Request has more book '%(value)s' than there are available. Please decrease."),
                        #     code='invalid',
                        #     params={'value': book.name},
                        # )
                        # form.add_error(NON_FIELD_ERRORS, message)
                    book.save()

            if basket.order_status == "in_process":
                if form.instance.order_status == "cancelled" or \
                   form.instance.order_status == "created":
                    goods_in_basket = models.GoodsInBasket.objects.filter(order=form.instance.pk)
                    for goods in goods_in_basket:
                        book = models.Book.objects.get(pk=goods.article.pk)
                        book.available += goods.quantity
                        book.save()
        return super().form_valid(form)


class DeleteBasket(PermissionRequiredMixin, generic.DeleteView):
    #   http://127.0.0.1:8000/bookstore/orders-delete/7
    permission_required = 'bookstore.delete_basket'
    model = models.Basket
    template_name = 'bookstore/orders_delete.html'
    success_url = reverse_lazy('bookstore:orders-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


# CRUDl GoodsInBasket:
class ShowGoodsInBasket(generic.ListView):  # not used for now
    #   http://127.0.0.1:8000/bookstore/goodsinbasket/
    model = models.GoodsInBasket
    template_name = 'bookstore/goodsinbasket_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        basket = None

        if self.request.user.is_authenticated:
            customer = self.request.user
            basket = models.Basket.objects.get(customer=customer)

        paginator = Paginator(basket.goodsinbaskets.all().order_by('name'), 3)  # Show 3 goods per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['basket'] = basket
        context['page_obj'] = page_obj
        return render(request, template_name='bookstore/goodsinbasket_list.html', context=context)


class CreateGoodsInBasket(View):
    #   http://127.0.0.1:8000/bookstore/goodsinbasket-create
    def post(self, request, *args, **kwargs):
        context = {}
        quantity = int(request.POST.get('quantity'))
        goods_pk = int(request.POST.get('goods_pk'))
        basket_id = int(request.session.get('basket_pk', 0))
        basket = None

        if goods_pk and quantity:
            if request.user.is_authenticated:
                customer = request.user
            else:
                customer = None
            if basket_id == 0:
                basket_id = None
            basket, created = models.Basket.objects.get_or_create(
                pk=basket_id,
                defaults={'customer': customer}
            )
            if created:
                request.session['basket_pk'] = basket.pk
            book = models.Book.objects.get(pk=goods_pk)
            goods_in_basket, created = models.GoodsInBasket.objects.get_or_create(
                order=basket,
                article=book,
                defaults={
                    'quantity': quantity,
                    'price': book.price,
                    'total_sum': quantity * book.price
                }
            )
            if not created:
                goods_in_basket.quantity += quantity
                goods_in_basket.total_sum += quantity * book.price
                goods_in_basket.save()

        context['basket'] = basket
        return render(request, template_name='bookstore/goodsinbasket_create.html', context=context)

    def get(self, request, *args, **kwargs):
        context = {}
        basket_id = int(request.session.get('basket_pk', 0))
        basket = None

        if basket_id:
            basket = models.Basket.objects.get(pk=basket_id)

        context['basket'] = basket
        return render(request, template_name='bookstore/goodsinbasket_create.html', context=context)


class UpdateGoodsInBasket(generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/goodsinbasket-update/7
    model = models.GoodsInBasket
    form_class = forms.GoodsInBasketForm
    template_name = 'bookstore/goodsinbasket_update.html'

    def get_success_url(self):
        update_basket_id = int(self.request.session.get('update_basket_id', 0))
        if update_basket_id:
            return reverse_lazy('bookstore:orders-update', kwargs={'pk': update_basket_id})
        else:
            return reverse_lazy('bookstore:goodsinbasket-create')

    def form_valid(self, form):
        goods_in_basket = models.GoodsInBasket.objects.get(pk=form.instance.pk)
        form.instance.total_sum += (form.instance.quantity - goods_in_basket.quantity) * form.instance.price
        return super().form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class DeleteGoodsInBasket(generic.DeleteView):
    #   http://127.0.0.1:8000/bookstore/goodsinbasket-delete/7
    model = models.GoodsInBasket
    template_name = 'bookstore/goodsinbasket_delete.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context

    def get_success_url(self):
        update_basket_id = int(self.request.session.get('update_basket_id', 0))
        if update_basket_id:
            return reverse_lazy('bookstore:orders-update', kwargs={'pk': update_basket_id})
        else:
            return reverse_lazy('bookstore:goodsinbasket-create')

    def form_valid(self, form):
        form_object = super().form_valid(form)

        update_basket_id = int(self.request.session.get('update_basket_id', 0))
        if update_basket_id:
            basket = models.Basket.objects.get(pk=update_basket_id)
            if len(basket.goodsinbaskets.all()) == 0:
                basket.delete()
                del self.request.session['update_basket_id']
                success_url = reverse_lazy('bookstore:orders-show')
                return HttpResponseRedirect(success_url)

        basket_id = int(self.request.session.get('basket_pk', 0))
        if basket_id:
            basket = models.Basket.objects.get(pk=basket_id)
            if len(basket.goodsinbaskets.all()) == 0:
                basket.delete()
                del self.request.session['basket_pk']
                success_url = reverse_lazy('bookstore:book-show')
                return HttpResponseRedirect(success_url)
        return form_object


class BasketComplete(generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/orders-complete
    model = models.Basket
    form_class = forms.BasketForm
    template_name = 'bookstore/orders_complete.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_success_url(self):
        del self.request.session['basket_pk']
        return reverse_lazy('bookstore:orders-complete-done')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        # basket_id = int(self.request.session.get('basket_pk', 0))
        #
        # if basket_id:
        #     basket = models.Basket.objects.get(pk=basket_id)
        #     if basket.customer:
        #         customer_data = models.Customer.objects.filter(user_data=basket.customer.id)
        #         if customer_data:
        #             customer_data = models.Customer.objects.get(user_data=basket.customer.id)
        #             object_temp = context.get('object')
        #             object_temp.contact_phone = customer_data.phone
        #             object_temp.order_country = customer_data.country
        #             object_temp.order_city = customer_data.city
        #             object_temp.order_zip_code = customer_data.zip_code
        #             object_temp.order_address1 = customer_data.address1
        #             object_temp.order_address2 = customer_data.address2
        #             object_temp.order_information = customer_data.information
        #             del context['form']
        #             context['form'] = forms.BasketForm(instance=object_temp, request=self.request)
        return context

    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            request,
            html_email_template_name=None,
    ):
        """
        Send a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context, request)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context, request)  ##  why tag is called here????
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")
        email_message.send()

    def form_valid(self, form):
        form.instance.order_status = 'created'
        subject_template_name = "bookstore/order_email_subject.txt"
        email_template_name = "bookstore/order_email_body.html"
        from_email = None
        to_email = ''
        for user in User.objects.filter(Q(groups__name="Managers")):
            to_email += user.email + ','
        local_context = {}
        current_site = get_current_site(self.request)
        domain = current_site.domain
        local_context['order_pk'] = form.instance.pk
        if self.request.is_secure():
            local_context['protocol'] = "https"
        else:
            local_context['protocol'] = "http"
        local_context['domain'] = domain
        self.send_mail(
            subject_template_name,
            email_template_name,
            local_context,
            from_email,
            to_email,
            self.request)
        return super().form_valid(form)


class OrderCompleteDone(generic.TemplateView):
    template_name = "bookstore/orders_success.html"


class SearchResult(View):
    #   http://127.0.0.1:8000/bookstore/books-search/?filterby=author&qfilter=ag
    def get(self, request, *args, **kwargs):
        context = {}
        # from django.contrib.sessions.models import Session
        # from django.contrib.sessions.backends.db import SessionStore
        # for ss in Session.objects.all():
        #     print(SessionStore().decode(ss.session_data))
        filterby = request.GET.get('filterby')
        qfilter = request.GET.get('qfilter')

        if filterby:
            self.request.session['filterby'] = filterby
        else:
            filterby = self.request.session.get('filterby')
        if qfilter:
            self.request.session['qfilter'] = qfilter
        else:
            qfilter = self.request.session.get('qfilter')
        object_list = None
        if filterby is None:
            object_list = models.Book.objects.filter(
                Q(name__icontains=qfilter) |
                Q(authors__name__icontains=qfilter) | Q(authors__surname__icontains=qfilter) |
                Q(series__name__icontains=qfilter) |
                Q(genre__name__icontains=qfilter) |
                Q(publisher__name__icontains=qfilter))

        if filterby == 'book':
            object_list = models.Book.objects.filter(
                Q(name__icontains=qfilter))

        if filterby == 'author':
            object_list = models.Book.objects.filter(
                Q(authors__name__icontains=qfilter) | Q(authors__surname__icontains=qfilter))

        if filterby == 'series':
            object_list = models.Book.objects.filter(
                Q(series__name__icontains=qfilter))

        if filterby == 'genre':
            object_list = models.Book.objects.filter(
                Q(genre__name__icontains=qfilter))

        if filterby == 'publisher':
            object_list = models.Book.objects.filter(
                Q(publisher__name__icontains=qfilter))

        filtered = " for '" + qfilter + "'"
        if filterby:
            filtered += ' in ' + filterby
        paginator = Paginator(object_list.order_by("name"), 3)  # Show 3 books per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
        context['page_obj'] = page_obj
        context['filtered'] = filtered
        return render(request, template_name='bookstore/book_list.html', context=context)


class SearchResultPK(View):
    #   http://127.0.0.1:8000/bookstore/books-search/series/1
    def get(self, request, *args, **kwargs):
        context = {}
        filterbypk = kwargs['fb']
        pk = kwargs['pk']
        object_list = None
        name = None
        filtered = None

        if filterbypk == 'author':
            object_list = models.Book.objects.filter(authors__pk=pk)
            author = Author.objects.get(pk=pk)
            name = author.name + "  " + author.surname

        if filterbypk == 'series':
            object_list = models.Book.objects.filter(series__pk=pk)
            name = Serie.objects.get(pk=pk).name

        if filterbypk == 'genre':
            object_list = models.Book.objects.filter(genre__pk=pk)
            name = Genre.objects.get(pk=pk).name

        if filterbypk == 'publisher':
            object_list = models.Book.objects.filter(publisher__pk=pk)
            name = Publisher.objects.get(pk=pk).name

        if name:
            filtered = " for " + filterbypk + " '" + name + "'"
        paginator = Paginator(object_list.order_by("name"), 3)  # Show 3 books per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['object_list'] = page_obj
        context['page_obj'] = page_obj
        context['filtered'] = filtered
        return render(request, template_name='bookstore/book_list.html', context=context)


# CRUD BasketComments:
class CreateBasketComments(PermissionRequiredMixin, generic.CreateView):  # not used for now
    #   http://127.0.0.1:8000/bookstore/basketcomments-create
    permission_required = 'bookstore.add_basketcomments'
    model = models.BasketComments
    form_class = forms.BasketCommentsForm
    template_name = 'bookstore/basketcomments_create.html'

    def form_valid(self, form):
        basket_pk = self.kwargs.get('basketpk')
        form.instance.basket = models.Basket.objects.get(pk=basket_pk)
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('bookstore:orders-detail', kwargs={'pk': self.object.basket.pk})


class UpdateBasketComments(PermissionRequiredMixin, generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/basketcomments-update/7
    permission_required = 'bookstore.change_basketcomments'
    model = models.BasketComments
    form_class = forms.BasketCommentsForm
    template_name = 'bookstore/basketcomments_update.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:orders-detail', kwargs={'pk': self.object.basket.pk})


class DeleteBasketComments(PermissionRequiredMixin, generic.DeleteView):
    #   http://127.0.0.1:8000/bookstore/basketcomments-delete/7
    permission_required = 'bookstore.delete_basketcomments'
    model = models.BasketComments
    template_name = 'bookstore/basketcomments_delete.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:orders-detail', kwargs={'pk': self.object.basket.pk})


# CRUD BookComments:
class CreateBookComments(PermissionRequiredMixin, generic.CreateView):
    #   http://127.0.0.1:8000/bookstore/bookcomments-create
    permission_required = 'bookstore.add_bookcomments'
    model = models.BookComments
    form_class = forms.BookCommentsForm
    template_name = 'bookstore/bookcomments_create.html'

    def form_valid(self, form):
        book_pk = self.kwargs.get('bookpk')
        book = models.Book.objects.get(pk=book_pk)
        form.instance.book = book
        form.instance.customer = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        book = models.Book.objects.get(pk=self.object.book.pk)
        book.rate = book.averagerate()
        book.save()
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.book.pk})


class UpdateBookComments(PermissionRequiredMixin, generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/bookcomments-update/7
    permission_required = 'bookstore.change_bookcomments'
    model = models.BookComments
    form_class = forms.BookCommentsForm
    template_name = 'bookstore/bookcomments_update.html'

    def get_success_url(self):
        book = models.Book.objects.get(pk=self.object.book.pk)
        book.rate = book.averagerate()
        book.save()
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.book.pk})


class DeleteBookComments(PermissionRequiredMixin, generic.DeleteView):
    #   http://127.0.0.1:8000/bookstore/bookcomments-delete/7
    permission_required = 'bookstore.delete_bookcomments'
    model = models.BookComments
    template_name = 'bookstore/bookcomments_delete.html'

    def get_success_url(self):
        return reverse_lazy('bookstore:book-detail', kwargs={'pk': self.object.book.pk})

    # def delete(self, request, *args, **kwargs):
    #     book = models.Book.objects.get(pk=self.object.book.pk)
    #     print('delete')
    #     answer = super().delete(self, request, *args, **kwargs)
    #     print('here')
    #     self.object.commit()
    #     book.averagerate()
    #     return answer

    def form_valid(self, form):
        book = models.Book.objects.get(pk=self.object.book.pk)
        form_object = super().form_valid(form)
        book.averagerate()
        return form_object
