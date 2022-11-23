from django.shortcuts import render
from . import models
from django.views.generic.edit import FormView
from django.views import View
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from . import models, forms


# Create your views here.
# CRUDl Books:
class ShowBook(generic.ListView):
    #   http://127.0.0.1:8000/bookstore/books
    model = models.Book
    template_name = 'bookstore/book_list.html'

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        basket = None

        if self.request.user.is_authenticated:
            customer = self.request.user
            basket = models.Basket.objects.filter(customer=customer)

        context['basket'] = basket
        return context


class ReadBasket(generic.DetailView):
    #   http://127.0.0.1:8000/bookstore/orders/2
    model = models.Basket
    template_name = 'bookstore/orders_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class UpdateBasket(generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/orders-update/7
    model = models.Basket
    form_class = forms.BasketForm
    template_name = 'bookstore/orders_update.html'

    def get_success_url(self):
        del self.request.session['update_basket_id']
        return reverse_lazy('bookstore:orders-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        self.request.session['update_basket_id'] = self.object.pk
        return context


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
class ShowGoodsInBasket(generic.ListView):
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

        context['basket'] = basket
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


class BasketComplete(generic.UpdateView):
    #   http://127.0.0.1:8000/bookstore/orders-complete
    model = models.Basket
    form_class = forms.BasketForm
    template_name = 'bookstore/orders_complete.html'

    def get_success_url(self):
        del self.request.session['basket_pk']
        return reverse_lazy('bookstore:orders-complete-done')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        basket_id = int(self.request.session.get('basket_pk', 0))

        if basket_id:
            basket = models.Basket.objects.get(pk=basket_id)
            if basket.customer:
                customer_data = models.Customer.objects.get(user_data=basket.customer.id)
                object_temp = context.get('object')
                object_temp.contact_phone = customer_data.phone
                object_temp.contact_phone = customer_data.phone
                object_temp.order_country = customer_data.country
                object_temp.order_city = customer_data.city
                object_temp.order_zip_code = customer_data.zip_code
                object_temp.order_address1 = customer_data.address1
                object_temp.order_address2 = customer_data.address2
                object_temp.order_information = customer_data.information
                context['form'] = forms.BasketForm(instance=object_temp)  #memory leak?? what happens with original form?
        return context

    def form_valid(self, form):
        form.instance.order_status = 'created'
        return super().form_valid(form)


class OrderCompleteDone(generic.TemplateView):
    template_name = "bookstore/orders_success.html"
