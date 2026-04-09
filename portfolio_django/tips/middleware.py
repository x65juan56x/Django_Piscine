import time
import random
from django.conf import settings


class AnonymousSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            return self.get_response(request)

        current_time = time.time()

        session_timestamp = request.session.get('name_timestamp', 0)

        if current_time - session_timestamp > 42:
            request.session['random_name'] = random.choice(settings.RANDOM_USER_NAMES)
            request.session['name_timestamp'] = current_time

            request.session.modified = True

        response = self.get_response(request)
        return response
