from django.contrib.auth.models import User
from toolkit.forms import CCEModelForm


class ProfileCreateForm(CCEModelForm):
    class Meta:
        model = User
        fields = (
            'user__first_name',
            'user__last_name',
            'user__username',
            'user__email',
            'user__password',
            'picture',
        )
