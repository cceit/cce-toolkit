from django import forms
from django.contrib.auth.models import User
from django.db import IntegrityError
from toolkit.forms import CCEModelForm

from profiles.models import Profile


class ProfileCreateForm(forms.Form):
    """
    Form for an applicant to register an account.
    """
    picture = forms.FileField(required=False)
    first_name = forms.CharField(max_length=30, help_text="30 characters or fewer.")
    last_name = forms.CharField(max_length=30, help_text="30 characters or fewer.")
    username = forms.CharField(max_length=30,
                               help_text="30 characters or fewer. Letters, digits and @/./+/-/_ only.")
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    email = forms.EmailField(max_length=254)

    def clean(self):
        cleaned_data = super(ProfileCreateForm, self).clean()
        try:
            match = cleaned_data['password'] == cleaned_data['confirm_password']
        except KeyError:
            pass
        else:
            if not match:
                self.add_error('confirm_password', 'Passwords must match.')
        return cleaned_data

    def create_user(self):
        """
        Create a user from cleaned_data and return it.
        Only called when the form data is valid.
        """
        # Make a user
        try:
            user = User.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],
            )
        except IntegrityError:  # e.g. duplicate username
            raise
        # Now add first and last names
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        Profile.objects.create(user=user)
        return user
