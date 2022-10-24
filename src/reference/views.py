from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from . import models, forms


# Create your views here.
def first(request):
    return HttpResponse(f"This is the default page. Try /admin, /ref/author, "
                        f"/ref/author-create, /ref/author-update, etc. for other options.")


# CRUDl Authors:
class ShowAuthors(generic.ListView):
    #   http://127.0.0.1:8000/ref/author
    model = models.Author
    template_name = 'reference/author_list.html'


class CreateAuthor(generic.CreateView):
    #   http://127.0.0.1:8000/ref/author-create
    model = models.Author
    form_class = forms.AuthorForm
    template_name = 'reference/author_create.html'

    def get_success_url(self):
        # return f'/ref/author/{self.object.pk}'
        return reverse_lazy('reference:author-detail', kwargs={'pk': self.object.pk})


class ReadAuthor(generic.DetailView):
    #   http://127.0.0.1:8000/ref/author/2
    model = models.Author
    template_name = 'reference/author_read.html'


class UpdateAuthor(generic.UpdateView):
    #   http://127.0.0.1:8000/ref/author-update/7
    model = models.Author
    form_class = forms.AuthorForm
    template_name = 'reference/author_update.html'

    def get_success_url(self):
        # return f'/ref-author/{self.object.pk}'
        return reverse_lazy('reference:author-detail', kwargs={'pk': self.object.pk})


class DeleteAuthor(generic.DeleteView):
    #   http://127.0.0.1:8000/ref/author-delete/7
    model = models.Author
    template_name = 'reference/author_delete.html'
    # success_url = f'/ref/author/'
    success_url = reverse_lazy('reference:author-show')


# CRUDl Series:
class ShowSerie(generic.ListView):
    #   http://127.0.0.1:8000/ref/series
    model = models.Serie
    template_name = 'reference/series_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'series'
        return context


class CreateSerie(generic.CreateView):
    #   http://127.0.0.1:8000/ref/series-create
    model = models.Serie
    form_class = forms.SerieForm
    template_name = 'reference/general_create.html'

    def get_success_url(self):
        return reverse_lazy('reference:series-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'series'
        return context

class ReadSerie(generic.DetailView):
    #   http://127.0.0.1:8000/ref/series/2
    model = models.Serie
    template_name = 'reference/general_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'series'
        context['ref_type_up'] = 'Series'
        context['ref_url'] = 'reference:series-show'
        return context


class UpdateSerie(generic.UpdateView):
    #   http://127.0.0.1:8000/ref/series-update/7
    model = models.Serie
    form_class = forms.SerieForm
    template_name = 'reference/general_update.html'

    def get_success_url(self):
        return reverse_lazy('reference:series-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'series'
        return context


class DeleteSerie(generic.DeleteView):
    #   http://127.0.0.1:8000/ref/series-delete/7
    model = models.Serie
    template_name = 'reference/general_delete.html'
    success_url = reverse_lazy('reference:series-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'series'
        context['ref_type_up'] = 'Series'
        return context


# CRUDl Genre:
class ShowGenre(generic.ListView):
    #   http://127.0.0.1:8000/ref/genre
    model = models.Genre
    template_name = 'reference/genre_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'genre'
        return context


class CreateGenre(generic.CreateView):
    #   http://127.0.0.1:8000/ref/genre-create
    model = models.Genre
    form_class = forms.GenreForm
    template_name = 'reference/general_create.html'

    def get_success_url(self):
        return reverse_lazy('reference:genre-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'genre'
        return context


class ReadGenre(generic.DetailView):
    #   http://127.0.0.1:8000/ref/genre/2
    model = models.Genre
    template_name = 'reference/general_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'genre'
        context['ref_type_up'] = 'Genre'
        context['ref_url'] = 'reference:genre-show'
        return context


class UpdateGenre(generic.UpdateView):
    #   http://127.0.0.1:8000/ref/genre-update/7
    model = models.Genre
    form_class = forms.GenreForm
    template_name = 'reference/general_update.html'

    def get_success_url(self):
        return reverse_lazy('reference:genre-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'genre'
        return context


class DeleteGenre(generic.DeleteView):
    #   http://127.0.0.1:8000/ref/genre-delete/7
    model = models.Genre
    template_name = 'reference/general_delete.html'
    success_url = reverse_lazy('reference:genre-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'genre'
        context['ref_type_up'] = 'Genre'
        return context


# CRUDl Publisher:
class ShowPublisher(generic.ListView):
    #   http://127.0.0.1:8000/ref/publish
    model = models.Publisher
    template_name = 'reference/publish_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'publisher'
        return context


class CreatePublisher(generic.CreateView):
    #   http://127.0.0.1:8000/ref/publish-create
    model = models.Publisher
    form_class = forms.PublisherForm
    template_name = 'reference/general_create.html'

    def get_success_url(self):
        return reverse_lazy('reference:publish-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'publisher'
        return context


class ReadPublisher(generic.DetailView):
    #   http://127.0.0.1:8000/ref/publish/2
    model = models.Publisher
    template_name = 'reference/general_read.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'publisher'
        context['ref_type_up'] = 'Publisher'
        context['ref_url'] = 'reference:publish-show'
        return context


class UpdatePublisher(generic.UpdateView):
    #   http://127.0.0.1:8000/ref/publish-update/7
    model = models.Publisher
    form_class = forms.PublisherForm
    template_name = 'reference/general_update.html'

    def get_success_url(self):
        return reverse_lazy('reference:publish-detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'publisher'
        return context


class DeletePublisher(generic.DeleteView):
    #   http://127.0.0.1:8000/ref/publish-delete/7
    model = models.Publisher
    template_name = 'reference/general_delete.html'
    success_url = reverse_lazy('reference:publish-show')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['ref_type'] = 'publisher'
        context['ref_type_up'] = 'Publisher'
        return context
