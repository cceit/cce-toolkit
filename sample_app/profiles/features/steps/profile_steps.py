from behave import step
from django.contrib.auth.models import User

from toolkit.helpers.bdd import fill_and_submit_form
from toolkit.helpers.bdd.shared_steps import *


@step("I submit valid registration information")
def register(context):
    b = context.browser

    fields = [
        {'function': 'fill', 'name': 'first_name', 'value': "Test"},
        {'function': 'fill', 'name': 'last_name', 'value': "Name"},
        {'function': 'fill', 'name': 'username', 'value': "Test Username"},
        {'function': 'fill', 'name': 'password', 'value': "asdf"},
        {'function': 'fill', 'name': 'confirm_password', 'value': "asdf"},
        {'function': 'fill', 'name': 'email', 'value': "asdf"},
    ]

    fill_and_submit_form(b, fields)


@step("I should be registered")
def check_for_registration(context):
    assert User.objects.get(pk=1).is_authenticated()


@step("I log in")
def log_in(context):
    b = context.browser

    fields = [
        {'function': 'fill', 'name': 'username', 'value': "mwilcoxen"},
        {'function': 'fill', 'name': 'password', 'value': "asdf"},
    ]

    fill_and_submit_form(b, fields, 'sign_in')


@step("I should be logged (in|out)")
def log_out(context, in_or_out):

    if in_or_out == "in":
        assert User.objects.get(pk=1).is_logged_in

    else:
        assert True

