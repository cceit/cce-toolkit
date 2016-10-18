import datetime
from django.conf import settings
from django.contrib import auth


class AutoLogout:
    def process_request(self, request):
        if not request.user.is_authenticated():
            # Can't log out if not logged in
            return

        try:
            inactive_period = datetime.datetime.now() - request.session['last_touch']
            auto_logout_delay = settings.AUTO_LOGOUT_DELAY if hasattr(settings, 'AUTO_LOGOUT_DELAY') else 60
            auto_logout_period = datetime.timedelta(minutes=auto_logout_delay)

            if inactive_period > auto_logout_period:
                auth.logout(request)
                del request.session['last_touch']
                return
        except KeyError:
            pass

        request.session['last_touch'] = datetime.datetime.now()
