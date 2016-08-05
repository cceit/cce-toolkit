from django.core.urlresolvers import reverse
from toolkit.views import CCECreateView

from profiles.forms import ProfileCreateForm
from profiles.models import Profile


class RegistrationView(CCECreateView):
    model = Profile
    form_class = ProfileCreateForm
    page_title = 'Register for DaBoard'
    sidebar_group = ['login']
    success_message = 'You have successfully registered for DaBoard'

    def get_success_url(self):
        return reverse('home')
