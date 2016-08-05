from toolkit.forms import CCEModelForm

from profiles.models import Profile


class ProfileCreateForm(CCEModelForm):
    class Meta:
        model = Profile
        fields = (
            'picture',
        )
