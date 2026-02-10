from django.shortcuts import render, redirect
from .models import Submission, TrapEvent
from django.views.decorators.csrf import csrf_exempt


def main_page(request):
    return render(request, 'main_page.html')


@csrf_exempt
def feedback_page(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        js_enabled = int(request.POST.get("js_enabled") or 0)
        time_on_page = int(request.POST.get("time_on_page") or 0)

        honeypot_input = request.POST.get("website", "")
        honeypot_textarea = request.POST.get("comment", "")

        xff = request.META.get("HTTP_X_FORWARDED_FOR")
        ip = xff.split(",")[0] if xff else request.META.get("REMOTE_ADDR")
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        referer = request.META.get("HTTP_REFERER")
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE")

        submission = Submission.objects.create(
            full_name=full_name,
            email=email,
            message=message,
            ip_address=ip,
            forwarded_ip=xff,
            user_agent=user_agent,
            accept_language=accept_language,
            request_method=request.method,
        )

        TrapEvent.objects.create(
            submission=submission,
            trap_type='HONEYPOT_INPUT',
            triggered=bool(honeypot_input.strip()),
            value=honeypot_input.strip()
        )

        TrapEvent.objects.create(
            submission=submission,
            trap_type='HONEYPOT_TEXTAREA',
            triggered=bool(honeypot_textarea.strip()),
            value=honeypot_textarea.strip()
        )

        TrapEvent.objects.create(
            submission=submission,
            trap_type='FAST_SUBMIT',
            triggered=time_on_page < 2,
            value=time_on_page
        )

        TrapEvent.objects.create(
            submission=submission,
            trap_type='JS_ENABLED',
            triggered=js_enabled != 1,
            value=js_enabled
        )

        TrapEvent.objects.create(
            submission=submission,
            trap_type='NO_REFERER',
            triggered=referer is None,
            value=referer
        )

        return redirect("feedback")

    return render(request, "feedback_page.html")


def neural_page(request):
    return render(request, 'neural_page.html')


def about_page(request):
    return render(request, 'about_page.html')


def secret_page(request):
    return render(request, 'secret_page.html')
