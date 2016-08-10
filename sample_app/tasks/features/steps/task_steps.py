import time
from behave import step

from tasks.models import Task
from toolkit.helpers.bdd import fill_and_submit_form
from toolkit.helpers.bdd.shared_steps import *


@step("I click the update status button")
def click_the_button(context):
    b = context.browser

    b.find_link_by_partial_href("/p/1/update_status").click()


@step("I click the view task button")
def click_view_button(context):
    b = context.browser

    b.find_link_by_partial_href("/p/1/").click()


@step("I update the status to (started|complete)")
def update_status(context, started_or_complete):
    b = context.browser

    if started_or_complete == "started":
        fields = [
            {'function': 'select', 'name': 'status', 'value': started_or_complete}
        ]

        fill_and_submit_form(b, fields)

    else:
        fields = [
            {'function': 'select', 'name': 'status', 'value': started_or_complete},
            {'function': 'fill', 'name': 'completed_at', 'value': "2016-08-10 12:00:00"}
        ]

        fill_and_submit_form(b, fields)


@step("The task status should be (started|complete)")
def check_status(context, started_or_completed):
    assert Task.objects.get(pk=1).status == started_or_completed
