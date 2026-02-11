from django.utils.deprecation import MiddlewareMixin
from django.http import Http404
from .models import ScanAttempt

class ScanDetectionMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            ip = get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            path = request.path
            referer = request.META.get("HTTP_REFERER", "")

            ScanAttempt.objects.create(
                ip_address=ip,
                user_agent=user_agent,
                requested_path=path,
                referer=referer
            )
        return response


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR')
