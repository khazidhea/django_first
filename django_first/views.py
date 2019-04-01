from django.http import HttpResponse


def hello(request):
    return HttpResponse('Hello, world!')


def bye(request):
    return HttpResponse('Bye, world!')
