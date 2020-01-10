from django.contrib.auth.models import AnonymousUser
from api.accesslogs.models import LogEntry
from django.conf import settings

class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.path in settings.ACCESS_LOG_EXEMPTIONS:
            return response

        log_entry = LogEntry(
            request_uri=request.path,
            request_meta=request.META,
            request_method=request.method,
            response_status_code=response.status_code
        )

        # Add the authenticated user, if it's available
        if not isinstance(request.user, AnonymousUser):
            log_entry.request_user_email = request.user.email
            log_entry.request_user_id = request.user.id

        log_entry.save()

        return response
