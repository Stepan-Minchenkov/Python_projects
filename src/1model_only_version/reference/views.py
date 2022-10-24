from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from . import models


# Create your views here.
# def show_authors(request):
#     #   http://127.0.0.1:8000/ref-author/?pk=2
#     authn = int(request.GET.get("pk"))
#     print(authn)
#     authors = models.Author.objects.filter(pk__gt=authn)
#     print(authors)
#     response = f'<h1> Authors for {request.user.username} with id > {authn}</h1>'
#     for author in authors:
#         response += f"Id: {author.pk} Author: {author.name} Surname: {author.surname} <br>"
#     return HttpResponse(response)

def show_authors(request):
    #   http://127.0.0.1:8000/ref-author/
    authors = models.Author.objects.all
    return render(request, template_name='reference/authors_list.html', context={'obj_list': authors})


def create_authors(request):
    #   http://127.0.0.1:8000/ref-author-create
    if request.method == "GET":
        return render(request, template_name='reference/author_create.html', context={})
    elif request.method == "POST":
        name_form = request.POST.get("name_form")
        surname_form = request.POST.get("surname_form")
        description_form = request.POST.get("desc_form")
        new_author = models.Author.objects.create(
            name=name_form,
            surname=surname_form,
            description=description_form)
        #  'ref-author/<int:pk>'
        return HttpResponseRedirect(f"/ref-author/{new_author.pk}")
    return HttpResponse("????????")


# def read_authors(request, pk: int):
#     #   http://127.0.0.1:8000/ref-author/2
#     auth_pk = pk
#     author = models.Author.objects.get(pk=auth_pk)
#     response = f'<h1> Information for author {request.user.username} with id = {auth_pk}</h1>'
#     response += f"Author: {author.name} Surname: {author.surname} <br>"
#     return HttpResponse(response)


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
        return render(request, template_name='reference/author_update.html', context={'obj_update': author})
    elif request.method == "POST":
        auth_pk = pk
        name_form = request.POST.get("name_form")
        surname_form = request.POST.get("surname_form")
        description_form = request.POST.get("desc_form")
        update_author = models.Author.objects.get(pk=auth_pk)
        update_author.name = name_form
        update_author.surname = surname_form
        update_author.description = description_form
        update_author.save()
        #  'ref-author/<int:pk>'
        return HttpResponseRedirect(f"/ref-author/{update_author.pk}")
    return HttpResponse("????????")


def delete_authors(request, pk: int):
    #   http://127.0.0.1:8000/ref-author-update/7
    if request.method == "GET":
        auth_pk = pk
        author = models.Author.objects.get(pk=auth_pk)
        return render(request, template_name='reference/author_delete.html', context={'obj_delete': author})
    elif request.method == "POST":
        auth_pk = pk
        models.Author.objects.get(pk=auth_pk).delete()
        #  'ref-author/'
        return HttpResponseRedirect(f"/ref-author/")

