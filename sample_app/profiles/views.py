from django.contrib import messages
from django.contrib.auth import login
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from toolkit.views import CCEFormView

from profiles.forms import ProfileCreateForm


class RegistrationView(CCEFormView):
    form_class = ProfileCreateForm
    page_title = 'Register for DaBoard'
    sidebar_group = ['login']
    success_message = 'You have successfully registered for DaBoard'
    template_name = 'form.html'

    def form_valid(self, form):
        """
        Create user, send activation email and log them in.
        """
        try:
            user = form.create_user()
        except IntegrityError:
            messages.warning(self.request, "That username is already in use. Please try another.")
            return self.form_invalid(form)
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_success_url(self):
        return reverse('home')
