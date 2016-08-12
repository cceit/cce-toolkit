from django.conf.urls import url

from profiles.views import RegistrationView

urlpatterns = [
    url(r'^register/', RegistrationView.as_view(), name="registration"),
]