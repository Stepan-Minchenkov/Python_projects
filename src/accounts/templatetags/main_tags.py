from django import template
from django.utils.safestring import mark_safe
import requests
import re
from django.conf import settings
from bookstore import models
from django.urls import reverse_lazy
# from django.contrib.sessions.models import Session
# from django.contrib.sessions.backends.db import SessionStore
import time
register = template.Library()


@register.simple_tag(takes_context=True)
def currency(context):
    # for ss in Session.objects.all():
    #     print(SessionStore().decode(ss.session_data))
    # refresh_time = 60 * 60 * 2   # in secs, so 2 hours = 60 * 60 * 2
    refresh_time = 60  # in secs, so 60 sec
    # print(context)
    exchange = 0
    # return mark_safe(exchange)  # temporary  --  for www.pythonanywhere.com

    request = context.get('request', 0)
    if not request:
        exchange = extract()
        return mark_safe(exchange)

    currency_time = request.session.get('currency_time', 0)
    exchange = request.session.get('exchange', 0)
    if currency_time and exchange and currency_time + refresh_time > time.time():
        return mark_safe(exchange)

    exchange = extract()
    if exchange:
        request.session['currency_time'] = time.time()
        request.session['exchange'] = exchange

    return mark_safe(exchange)


def extract():
    exchange_value = 0
    r = requests.get(settings.NBRBBY)
    if r.status_code == 200:
        # For nbrb.by
        pos = r.text.find('<span class="text">Доллар США</span>')
        if pos > 0:
            pos1 = r.text.find('curCours', pos)
            if pos1 > 0:
                pos2 = r.text.find('</div>', pos1)
                exchange_value = re.split('<+|>', r.text[pos1:pos2])[-1]
        # For mtbank.by
        # pos = r.text.find('<span class="rates-card__title">1 Доллар США</span>')
        # if pos > 0:
        #     pos1 = r.text.find('rates-card__number', pos)
        #     if pos1 > 0:
        #         pos2 = r.text.find('</span>', pos1)
        #         exchange_value = re.split('<+|>', r.text[pos1:pos2])[-1]
    return exchange_value


@register.simple_tag(takes_context=True)
def in_cart(context):
    cart = 0
    request = context.get('request', 0)
    if not request:
        return mark_safe(cart)

    basket_id = int(request.session.get('basket_pk', 0))
    if basket_id:
        basket = models.Basket.objects.get(pk=basket_id)
        cart = basket.total_books_number()
    return mark_safe(cart)


@register.simple_tag()
def currency_url():
    return mark_safe(settings.NBRBBY)


@register.simple_tag(takes_context=True)
def in_cart_url(context):
    url = ''
    request = context.get('request', 0)
    if not request:
        return mark_safe(url)

    basket_id = int(request.session.get('basket_pk', 0))
    if basket_id:
        url = reverse_lazy('bookstore:orders-complete', kwargs={'pk': basket_id})
    return mark_safe(url)
