import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .models import Submission, TrapEvent, TrapLink, CaptchaEvent
from django.views.decorators.csrf import csrf_exempt


def main_page(request):
    return render(request, 'main_page.html')


@csrf_exempt
def feedback_page_1(request):
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
            triggered=time_on_page <= 2,
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

        return redirect("feedback-1")

    return render(request, "feedback_page_1.html")


@csrf_exempt
def feedback_page_2(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        time_on_page = int(request.POST.get("time_on_page") or 0)
        js_enabled = int(request.POST.get("js_enabled") or 0)

        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE")

        captcha_token = request.POST.get("g-recaptcha-response")
        captcha_success = False
        if captcha_token:
            url = "https://www.google.com/recaptcha/api/siteverify"
            payload = {
                "secret": settings.GOOGLE_SITE_PRIVATE_KEY,
                "response": captcha_token
            }
            resp = requests.post(url, data=payload)
            result = resp.json()
            captcha_success = result.get("success", False)

        submission = Submission.objects.create(
            full_name=full_name,
            email=email,
            message=message,
            ip_address=ip,
            forwarded_ip=request.META.get("HTTP_X_FORWARDED_FOR"),
            user_agent=user_agent,
            accept_language=accept_language,
            request_method=request.method,
        )

        from .models import CaptchaEvent
        CaptchaEvent.objects.create(
            submission=submission,
            captcha_type="google",
            success=captcha_success,
            time_on_page=time_on_page,
            js_enabled=True if js_enabled == 1 else False
        )

        return redirect("feedback-2")

    return render(request, "feedback_page_2.html", {
        "GOOGLE_SITE_PUBLIC_KEY": settings.GOOGLE_SITE_PUBLIC_KEY
    })


@csrf_exempt
def feedback_page_3(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        time_on_page = int(request.POST.get("time_on_page") or 0)
        js_enabled = int(request.POST.get("js_enabled") or 0)

        ip = get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")
        accept_language = request.META.get("HTTP_ACCEPT_LANGUAGE")

        token = request.POST.get("cf-turnstile-response")
        success = False
        if token:
            url = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
            payload = {
                "secret": settings.CLOUDFLARE_SITE_PRIVATE_KEY,
                "response": token,
                "remoteip": ip
            }
            resp = requests.post(url, data=payload)
            result = resp.json()
            success = result.get("success", False)

        submission = Submission.objects.create(
            full_name=full_name,
            email=email,
            message=message,
            ip_address=ip,
            forwarded_ip=request.META.get("HTTP_X_FORWARDED_FOR"),
            user_agent=user_agent,
            accept_language=accept_language,
            request_method=request.method,
        )

        CaptchaEvent.objects.create(
            submission=submission,
            captcha_type="cloudflare",
            success=success,
            time_on_page=time_on_page,
            js_enabled=js_enabled != 0
        )

        return redirect("feedback-3")

    return render(request, "feedback_page_3.html", {
        "CLOUDFLARE_SITE_PRIVATE_KEY": settings.CLOUDFLARE_SITE_PRIVATE_KEY
    })


def neural_page(request):
    return render(request, 'neural_page.html')


def about_page(request):
    return render(request, 'about_page.html')


def secret_page(request):

    trap = request.GET.get("name")
    trap_type = request.GET.get("type")
    source = request.GET.get("source")
    

    if trap and trap_type:
        TrapLink.objects.create(
            ip_address=get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", ""),
            trap_name=trap,
            trap_category=get_category(trap),
            trap_type=trap_type,
            source_page=source,
            referer=request.META.get("HTTP_REFERER")
        )

    return render(request, 'secret_page.html')


def get_category(trap):
    mapping = {
        "internal": "debug",
        "debug": "debug",
        "trace": "debug",
        "debug-console": "debug",
        "test-panel": "debug",
        "logs": "debug",

        "administrator": "admin",
        "control-panel": "admin",
        "admin-dashboard": "admin",
        "administrator-panel": "admin",
        "admin-panel": "admin",
        "management": "admin",

        "app-config": "config",
        "site-settings": "config",
        "settings": "config",
        "config": "config",
        "env": "config",
        "system-config": "config",

        "archive": "backup",
        "database-dump": "backup",
        "backup-old": "backup",
        "backup": "backup",
        "db-backup": "backup",
        "data-dump": "backup",
    }
    return mapping.get(trap, "unknown")


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')