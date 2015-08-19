from django.core.urlresolvers import reverse, NoReverseMatch
from behave import *
import requests

from splinter.exceptions import ElementDoesNotExist
from toolkit.test_tools.bdd_test_helpers import get_file_content_type, fill_and_submit_form

__all__ = ['log_in_as', 'visit_page', 'verify_navigation', 'verify_file_received']

use_step_matcher("re")


@given('I am logged in as (.*)')
def log_in_as(context, user):
    b = context.browser
    b.visit(context.server_url + reverse('login'))

    fields = [
        {'function': 'fill', 'name': 'username', 'value': user},
        {'function': 'fill', 'name': 'password', 'value': user},
    ]

    fill_and_submit_form(b, fields, 'sign_in')


@when("I visit (.*)")
def visit_page(context, url_name):
    b = context.browser

    try:
        url = context.server_url + reverse(url_name)
    except NoReverseMatch:
        try:
            url = context.server_url + reverse(url_name, kwargs={'pk': context.test_obj.pk})
        except AttributeError:
            raise Exception("%s not found. Check the url config." % url_name)

    context.result = requests.get(url, cookies=b.cookies.all())
    b.visit(url)


@then("I should find a link to (.*)")
def verify_navigation(context, url_names):
    b = context.browser

    urls = [url.strip() for url in url_names.split(',')]  # Creates a list of the arbitrary number of url_names captured
    for url in urls:
        try:
            link = reverse(url)
        except NoReverseMatch:
            try:
                link = reverse(url, kwargs={'pk': context.test_obj.pk})
            except:
                raise Exception("Unable to find link for '%s'" % url)  # Use try/catch/raise when asserts don't cut it

        try:
            b.find_link_by_partial_href(str(link))[0]  # Accessing a missing element throws ElementDoesNotExist
        except ElementDoesNotExist:
            raise Exception("Unable to find link for '%s'" % url)  # Use try/catch/raise when asserts don't cut it


@then("I should( not)? find a form that posts to (.*)")
def verify_post_form(context, should_not, url_name):
    try:
        link = reverse(url_name)
    except NoReverseMatch:
        try:
            link = reverse(url_name, kwargs={'pk': context.test_obj.pk})
        except:
            raise Exception("Unable to reverse lookup '%s'" % url_name)
    css_string = 'form[action="%s"]' % link
    if should_not:
        try:
            context.browser.find_by_css(css_string)[0]
        except ElementDoesNotExist:
            pass
        else:
            raise Exception("Unexpectedly found form that posts to %s" % link)
    else:
        try:
            context.browser.find_by_css(css_string)[0]
        except ElementDoesNotExist:
            raise Exception("Unable to find form that posts to %s" % link)


@then("I should receive a (.*) file download")
def verify_file_received(context, file_type):
    received_type = context.result.headers['content-type']
    target_type = get_file_content_type(file_type)
    assert received_type == target_type, "%s != %s" % (received_type, target_type)
