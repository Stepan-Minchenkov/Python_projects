from django.urls import path
from . import views as bookstore_views

app_name = 'bookstore'
urlpatterns = [
    path('books/<int:pk>', bookstore_views.ReadBook.as_view(), name='book-detail'),
    path('books/', bookstore_views.ShowBook.as_view(), name='book-show'),
    path('books-create/', bookstore_views.CreateBook.as_view(), name='book-create'),
    path('books-delete/<int:pk>', bookstore_views.DeleteBook.as_view(), name='book-delete'),
    path('books-update/<int:pk>', bookstore_views.UpdateBook.as_view(), name='book-update'),

    # path('goodsinbasket/', bookstore_views.ShowGoodsInBasket.as_view(), name='goodsinbasket-show'),
    path('goodsinbasket-create/', bookstore_views.CreateGoodsInBasket.as_view(), name='goodsinbasket-create'),
    path('goodsinbasket-delete/<int:pk>', bookstore_views.DeleteGoodsInBasket.as_view(), name='goodsinbasket-delete'),
    path('goodsinbasket-update/<int:pk>', bookstore_views.UpdateGoodsInBasket.as_view(), name='goodsinbasket-update'),

    path('orders/', bookstore_views.ShowBasket.as_view(), name='orders-show'),
    # path('orders-create/', bookstore_views.CreateBasket.as_view(), name='orders-create'),
    path('orders/<int:pk>', bookstore_views.ReadBasket.as_view(), name='orders-detail'),
    path('orders-delete/<int:pk>', bookstore_views.DeleteBasket.as_view(), name='orders-delete'),
    path('orders-update/<int:pk>', bookstore_views.UpdateBasket.as_view(), name='orders-update'),
    path('orders-complete/<int:pk>', bookstore_views.BasketComplete.as_view(), name='orders-complete'),
    path('orders-complete/', bookstore_views.OrderCompleteDone.as_view(), name='orders-complete-done'),

    path('books-search/<str:fb>/<int:pk>', bookstore_views.SearchResultPK.as_view(), name='book-search-pk'),
    path('books-search/', bookstore_views.SearchResult.as_view(), name='book-search'),

    path('ordercomments-create/<int:basketpk>', bookstore_views.CreateBasketComments.as_view(),
         name='ordercomments-create'),
    path('ordercomments-delete/<int:pk>', bookstore_views.DeleteBasketComments.as_view(), name='ordercomments-delete'),
    path('ordercomments-update/<int:pk>', bookstore_views.UpdateBasketComments.as_view(), name='ordercomments-update'),

    path('bookcomments-create/<int:bookpk>', bookstore_views.CreateBookComments.as_view(),
         name='bookcomments-create'),
    path('bookcomments-delete/<int:pk>', bookstore_views.DeleteBookComments.as_view(), name='bookcomments-delete'),
    path('bookcomments-update/<int:pk>', bookstore_views.UpdateBookComments.as_view(), name='bookcomments-update'),
]
