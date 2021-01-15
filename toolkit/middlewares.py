import datetime
from threading import get_ident

from django.conf import settings
from django.contrib import auth


class AutoLogout(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        return self.get_response(request)

    def process_request(self, request):
        if not request.user.is_authenticated:
            # Can't log out if not logged in
            return None

        try:
            inactive_period = datetime.datetime.now() - request.session['last_touch']
            auto_logout_delay = settings.AUTO_LOGOUT_DELAY if hasattr(settings, 'AUTO_LOGOUT_DELAY') else 60
            auto_logout_period = datetime.timedelta(minutes=auto_logout_delay)

            if inactive_period > auto_logout_period:
                auth.logout(request)
                del request.session['last_touch']
                return None
        except KeyError:
            pass

        request.session['last_touch'] = datetime.datetime.now()
        return None


class GlobalRequest(object):
    _threadmap = {}
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    @classmethod
    def get_current_request(cls):
        return cls._threadmap.get(get_ident(), None)

    def process_request(self, request):
        self._threadmap[get_ident()] = request

    def process_exception(self, request, exception):
        try:
            del self._threadmap[get_ident()]
        except KeyError:
            pass

    def process_response(self, request, response):
        try:
            del self._threadmap[get_ident()]
        except KeyError:
            pass
        return response