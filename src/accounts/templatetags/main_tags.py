from django import template
from django.utils.safestring import mark_safe
import requests
import re
from django.conf import settings
from bookstore import models
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
    request = context['request']
    currency_time = request.session.get('currency_time', 0)
    exchange = request.session.get('exchange', 0)
    if currency_time and exchange and currency_time + refresh_time > time.time():
        return mark_safe(exchange)

    r = requests.get(settings.NBRBBY)
    if r.status_code == 200:
        pos = r.text.find('<span class="text">Доллар США</span>')
        if pos > 0:
            pos1 = r.text.find('curCours', pos)
            if pos1 > 0:
                pos2 = r.text.find('</div>', pos1)
                exchange = re.split('<+|>', r.text[pos1:pos2])[-1]
                currency_time = time.time()
                request.session['currency_time'] = currency_time
                request.session['exchange'] = exchange
    return mark_safe(exchange)


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


@register.simple_tag(takes_context=True)
def currency_url(context):
    return mark_safe(settings.NBRBBY)
