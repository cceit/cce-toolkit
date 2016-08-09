import decimal
from behave import *

from django.conf import settings
from django.contrib.auth.models import User

from toolkit.helpers.bdd.shared_steps import *

from toolkit.helpers.bdd import fill_and_submit_form
from boards.models import Board


@step("I submit valid (registration|board|plank|splinter) information")
def create_profile(context, target_variable):
    context.board_name = "Test Board"
    context.board_description = "Test Description"
    context.plank_title = "Test Plank"
    context.splinter_comment = "Test Splinter Comment"

    if target_variable == "regiestration":
        b = context.browser

        fields = [
            {'function': 'fill', 'name': 'first_name', 'value': "Mark"},
            {'function': 'fill', 'name': 'last_name', 'value': "Wilcoxen"},
            {'function': 'fill', 'name': 'username', 'value': "mwilcoxen"},
            {'function': 'fill', 'name': 'password', 'value': "asdf"},
            {'function': 'fill', 'name': 'confirm_password', 'value': "asdf"},
            {'function': 'fill', 'name': 'email', 'value': "Test@test.com"},
        ]

        fill_and_submit_form(b, fields)

    elif target_variable == "board":
        return None
    elif target_variable == "plank":
        return None
    else:
        return None


@step("I should be registered")
def check_for_registration(context):
    assert User.objects.get(pk=1).is_authenticated()


@then("I should see the (board|plank|splinter)")
def check_for_object(context, target_variable):
    b = context.browser
    expected_count = 1

    if target_variable == "board":
        assert Board.objects.filter(name=context.board_name).count() == expected_count
        assert b.is_text_present(context.board_name)