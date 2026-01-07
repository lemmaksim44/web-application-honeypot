from django.http import HttpResponse
from django.template import loader


def main_page(request):
    template = loader.get_template('main_page.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def feedback_page(request):
    template = loader.get_template('feedback_page.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def neural_page(request):
    template = loader.get_template('neural_page.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)


def about_page(request):
    template = loader.get_template('about_page.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)

def secret_page(request):
    template = loader.get_template('secret_page.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)