from django.contrib.auth.models import User
from bookstore.models import Book, GoodsInBasket, Basket, Customer
from reference.models import Author, Serie, Genre, Publisher

user = User.objects.create_user('First', password='first1234', email='qq1@mail.ru')
b = Customer(user_data=user, phone='123-456', country='BLR',
             city='Minsk', zip_code='22wwww', address1='a', address2='b', information='s')
b.save()

user = User.objects.create_user('Second', password='second1234', email='qq2@mail.ru')
b = Customer(user_data=user, phone='123-456', country='BLR',
             city='Minsk', zip_code='22wwww', address1='a', address2='b', information='s')
b.save()

author = Author.objects.get(name='Agatha')
serie = Serie.objects.get(name='Эркюль Пуаро')
genre = Genre.objects.get(name='Детективы')
publisher = Publisher.objects.get(name='ACT')
Book.objects.create(
    name='Убийство в Восточном экспрессе',
    price=23.44,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2021',
    number_of_pages=144,
    cover='твердый',
    book_format='A5',
    ISBN='1-2-3-4',
    weight=300,
    allowed_age=10,
    publisher=publisher,
    available=20,
    active=True,
    rate=0)

Book.objects.create(
    name='Загадка Эндхауза',
    price=19.04,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2020',
    number_of_pages=121,
    cover='твердый',
    book_format='A5',
    ISBN='1-2-3-6',
    weight=250,
    allowed_age=10,
    publisher=publisher,
    available=30,
    active=True,
    rate=0)


Book.objects.create(
    name='Рождество Эркюля Пуаро',
    price=29.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2022',
    number_of_pages=102,
    cover='мягкий',
    book_format='A5',
    ISBN='4-2-3-6',
    weight=190,
    allowed_age=10,
    publisher=publisher,
    available=13,
    active=True,
    rate=0)

publisher = Publisher.objects.get(name='Эксмо')
Book.objects.create(
    name='Миссис Макгинти с жизнью рассталась',
    price=9.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2021',
    number_of_pages=102,
    cover='мягкий',
    book_format='A6',
    ISBN='7-2-3-6',
    weight=110,
    allowed_age=10,
    publisher=publisher,
    available=3,
    active=True,
    rate=0)

publisher = Publisher.objects.get(name='Pinguin Publishing')
Book.objects.create(
    name='The Murder on the Links',
    price=39.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2019',
    number_of_pages=120,
    cover='мягкий',
    book_format='A6',
    ISBN='234-2-3-611',
    weight=120,
    allowed_age=10,
    publisher=publisher,
    available=5,
    active=True,
    rate=0)

author = Author.objects.get(name='Artur Conan')
serie = Serie.objects.get(name='Шерлок Холмс')
genre = Genre.objects.get(name='Детективы')
publisher = Publisher.objects.get(name='ACT')
Book.objects.create(
    name='Весь Шерлок Холмс',
    price=109.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2022',
    number_of_pages=1200,
    cover='твердый',
    book_format='A5',
    ISBN='671-2-3-674',
    weight=2000,
    allowed_age=10,
    publisher=publisher,
    available=2,
    active=True,
    rate=0)

publisher = Publisher.objects.get(name='Эксмо')
Book.objects.create(
    name='Собака Баскервилей',
    price=19.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2012',
    number_of_pages=100,
    cover='мягкий',
    book_format='A6',
    ISBN='671-2-553-64',
    weight=200,
    allowed_age=10,
    publisher=publisher,
    available=7,
    active=True,
    rate=0)

publisher = Publisher.objects.get(name='Harper Collins')
Book.objects.create(
    name='The Hound of the Baskervilles',
    price=49.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2008',
    number_of_pages=100,
    cover='мягкий',
    book_format='A6',
    ISBN='671-2-553-614',
    weight=200,
    allowed_age=10,
    publisher=publisher,
    available=1,
    active=True,
    rate=0)

author = Author.objects.get(name='Эдит')
serie = Serie.objects.get(name='Пять юных сыщиков и верный пес')
genre = Genre.objects.get(name='Литература для детей')
publisher = Publisher.objects.get(name='Эксмо')
Book.objects.create(
    name='Тайна сгоревшего коттеджа',
    price=19.00,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2019',
    number_of_pages=256,
    cover='твердый',
    book_format='A5',
    ISBN='978-5-389-15889-4',
    weight=300,
    allowed_age=10,
    publisher=publisher,
    available=12,
    active=True,
    rate=0)

Book.objects.create(
    name='Тайна ограбления в театре',
    price=19.00,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2021',
    number_of_pages=192,
    cover='твердый',
    book_format='A5',
    ISBN='978-5-389-18559-3',
    weight=253,
    allowed_age=10,
    publisher=publisher,
    available=15,
    active=True,
    rate=0)

serie = Serie.objects.get(name='Великолепная пятерка')
publisher = Publisher.objects.get(name='ACT')
Book.objects.create(
    name='Тайна серебристого лимузина',
    price=9.99,
    authors=author,
    series=serie,
    genre=genre,
    publish_year='2007',
    number_of_pages=240,
    cover='твердый',
    book_format='A5',
    ISBN='978-5-389-15413-1',
    weight=292,
    allowed_age=10,
    publisher=publisher,
    available=10,
    active=True,
    rate=0)

