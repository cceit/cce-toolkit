from django.core.urlresolvers import reverse, NoReverseMatch
from behave import *
import requests

from splinter.exceptions import ElementDoesNotExist
from toolkit.helpers.bdd import fill_and_submit_form, compare_content_types

__all__ = [
    'log_in_as',
    'visit_page',
    'verify_navigation',
    'verify_post_form',
    'verify_file_download',
]

use_step_matcher("re")


@given('I am logged in as (.*)')
def log_in_as(context, user):
    b = context.browser
    context.user = user
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


@then("I (should|shouldn't) receive a (.*) file download")
def verify_file_download(context, should_or_shouldnt, file_type):
    target_type, received_type = compare_content_types(context.browser, context, file_type)
    if should_or_shouldnt == 'should':
        assert received_type == target_type, "%s != %s" % (received_type, target_type)
    elif should_or_shouldnt == "shouldn't":
        try:
            error = context.browser.find_by_css('.alert-error').first
        except ElementDoesNotExist:
            raise AssertionError("Expected to see errors, but didn't.")
        else:
            assert error.visible, "Expected to see errors, but didn't."

        assert received_type != target_type, "File found in response."
    else:
        raise NotImplementedError

