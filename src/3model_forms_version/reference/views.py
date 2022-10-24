from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models, forms


# Create your views here.
def first(request):
    return HttpResponse(f"This is the default page. Try /admin, /ref-author, "
                        f"/ref-author-create, /ref-author-update, etc. for other options.")


def show_authors(request):
    #   http://127.0.0.1:8000/ref-author/
    authors = models.Author.objects.all
    return render(request, template_name='reference/authors_list.html', context={'obj_list': authors})


def create_authors(request):
    #   http://127.0.0.1:8000/ref-author-create
    if request.method == "GET":
        author_form = forms.AuthorForm()
        context = {'form_create': author_form}
        return render(request, template_name='reference/author_create.html', context=context)
    elif request.method == "POST":
        author_form = forms.AuthorForm(request.POST)
        if author_form.is_valid():
            new_author = author_form.save()
            #  'ref-author/<int:pk>'
            return HttpResponseRedirect(f"/ref-author/{new_author.pk}")
        else:
            context = {'form_create': author_form}
            return render(request, template_name='reference/author_create.html', context=context)
    return HttpResponse("????????")


def read_authors(request, pk: int):
    #   http://127.0.0.1:8000/ref-author/2
    auth_pk = pk
    author = models.Author.objects.get(pk=auth_pk)
    return render(request, template_name='reference/author_read.html', context={'obj_read': author})


def update_authors(request, pk: int):
    #   http://127.0.0.1:8000/ref-author-update/7
    if request.method == "GET":
        auth_pk = pk
        author = models.Author.objects.get(pk=auth_pk)
        author_form = forms.AuthorForm(instance=author)
        context = {'form_update': author_form}
        return render(request, template_name='reference/author_update.html', context=context)
    elif request.method == "POST":
        auth_pk = pk
        update_author = models.Author.objects.get(pk=auth_pk)
        author_form = forms.AuthorForm(request.POST, instance=update_author)
        if author_form.is_valid():
            author_form.save()
            #  'ref-author/<int:pk>'
            return HttpResponseRedirect(f"/ref-author/{update_author.pk}")
        else:
            context = {'form_update': author_form}
            return render(request, template_name='reference/author_update.html', context=context)
    return HttpResponse("????????")


def delete_authors(request, pk: int):
    #   http://127.0.0.1:8000/ref-author-delete/7
    if request.method == "GET":
        auth_pk = pk
        author = models.Author.objects.get(pk=auth_pk)
        return render(request, template_name='reference/author_delete.html', context={'obj_delete': author})
    elif request.method == "POST":
        auth_pk = pk
        models.Author.objects.get(pk=auth_pk).delete()
        #  'ref-author/'
        return HttpResponseRedirect(f"/ref-author/")

