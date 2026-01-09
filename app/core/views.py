from django.shortcuts import render, redirect
from .models import Feedback


def main_page(request):
    return render(request, 'main_page.html')


def feedback_page(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        Feedback.objects.create(
            full_name=full_name,
            email=email,
            message=message
        )

        return redirect("feedback")

    return render(request, 'feedback_page.html')


def neural_page(request):
    return render(request, 'neural_page.html')


def about_page(request):
    return render(request, 'about_page.html')


def secret_page(request):
    return render(request, 'secret_page.html')
