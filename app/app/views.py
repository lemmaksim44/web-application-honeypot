from django.http import HttpResponse
from django.template import loader

def main_page(request):
    template = loader.get_template('main_page.html')
    context = {}
    rendered_page = template.render(context, request)
    return HttpResponse(rendered_page)
