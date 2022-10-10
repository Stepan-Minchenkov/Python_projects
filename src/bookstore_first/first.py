from django.http import HttpResponse


def first(request):
    return HttpResponse(f"This is the default page. Try /admin or /Hi for other options.")
