from django.urls import path

from . import views as ref_view

app_name = 'reference'
urlpatterns = [
    path('author/<int:pk>', ref_view.ReadAuthor.as_view(), name='author-detail'),
    path('author/', ref_view.ShowAuthors.as_view(), name='author-show'),
    path('author-create/', ref_view.CreateAuthor.as_view(), name='author-create'),
    path('author-delete/<int:pk>', ref_view.DeleteAuthor.as_view(), name='author-delete'),
    path('author-update/<int:pk>', ref_view.UpdateAuthor.as_view(), name='author-update'),

    path('series/<int:pk>', ref_view.ReadSerie.as_view(), name='series-detail'),
    path('series/', ref_view.ShowSerie.as_view(), name='series-show'),
    path('series-create/', ref_view.CreateSerie.as_view(), name='series-create'),
    path('series-delete/<int:pk>', ref_view.DeleteSerie.as_view(), name='series-delete'),
    path('series-update/<int:pk>', ref_view.UpdateSerie.as_view(), name='series-update'),

    path('genre/<int:pk>', ref_view.ReadGenre.as_view(), name='genre-detail'),
    path('genre/', ref_view.ShowGenre.as_view(), name='genre-show'),
    path('genre-create/', ref_view.CreateGenre.as_view(), name='genre-create'),
    path('genre-delete/<int:pk>', ref_view.DeleteGenre.as_view(), name='genre-delete'),
    path('genre-update/<int:pk>', ref_view.UpdateGenre.as_view(), name='genre-update'),

    path('publish/<int:pk>', ref_view.ReadPublisher.as_view(), name='publish-detail'),
    path('publish/', ref_view.ShowPublisher.as_view(), name='publish-show'),
    path('publish-create/', ref_view.CreatePublisher.as_view(), name='publish-create'),
    path('publish-delete/<int:pk>', ref_view.DeletePublisher.as_view(), name='publish-delete'),
    path('publish-update/<int:pk>', ref_view.UpdatePublisher.as_view(), name='publish-update')
]
