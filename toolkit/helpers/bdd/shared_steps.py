from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, NoReverseMatch
from behave import *
import requests

from splinter.exceptions import ElementDoesNotExist
from bdd import fill_and_submit_form, compare_content_types

__all__ = [
    'log_in_as',
    'visit_page',
    'verify_navigation',
    'verify_post_form',
    'verify_file_download',
    'confirm_success_message',
    'assert_text_on_page',
]

use_step_matcher("re")


@given('I am logged in as (.*)')
def log_in_as(context, user):
    """Allows you to log in as a user in the system.
    I am logged in as (.*)

    :param object  context: behave's global object
    :param string user: user in the system


    Usage:
        .. code-block:: python
            :linenos:

            Scenario Outline: Manage applications
                Given I am logged in as manager

    """
    b = context.browser
    context.user = User.objects.get(username=user)
    context.user.is_active = True
    context.user.save()

    b.visit(context.server_url + reverse('login'))

    fields = [
        {'function': 'fill', 'name': 'username', 'value': user},
        {'function': 'fill', 'name': 'password', 'value': user},
    ]

    fill_and_submit_form(b, fields, 'sign_in')


@when("I visit (.*)")
def visit_page(context, url_name):
    """Allows you to visit a page in the system. I visit (.*)


    :param object  context: behave's global object
    :param string url_name: url name to visit


    Usage:
        .. code-block:: python
            :linenos:

            Scenario Outline: Manage applications
                Given I am logged in as manager
                When I visit manage_application

    """
    b = context.browser

    try:
        url = context.server_url + reverse(url_name)
    except NoReverseMatch:
        try:
            url = context.server_url + reverse(url_name, kwargs={'pk': context.test_obj.pk})
        except AttributeError:
            raise Exception("%s not found. Check the url config." % url_name)

    try:
        context.result = requests.get(url, cookies=b.cookies.all())
    except KeyError:
        pass
    b.visit(url)


@then("I should find a link to (.*)")
def verify_navigation(context, url_names):
    """Allows you to find a link on the current page


    :param object  context: behave's global object
    :param string url_names: url name(s) to visit, add comma between url name if there's more than one


    Usage:
        .. code-block:: python
            :linenos:

            Scenario Outline: Manage applications
                Given I am logged in as manager
                When I visit manage_application
                Then I should find a link to add_application

    """
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
    """Allows you know if there's a form that can be posted to a certain place on the page.
    I should( not)? find a form that posts to (.*)


    :param object  context: behave's global object
    :param string should_not: include "not" if the form should not be found
    :param string url_name: url name to visit


    Usage 1:
        .. code-block:: python
            :linenos:

            Scenario Outline: Manage applications
                Given I am logged in as manager
                And I have a valid submitted application
                When I visit view_application
                Then I should find a form that posts to approve_application


    Usage 2:
        .. code-block:: python
            :linenos:

            Scenario Outline: Manage applications
                Given I am logged in as manager
                And I have a valid application
                When I visit view_application
                Then I should not find a form that posts to approve_application

    """
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
    """Allows you to compare the file download type. I (should|shouldn't) receive a (.*) file download


    :param object  context: behave's global object
    :param string should_or_shouldnt: should or shouldn't
    :param string file_type: file type


    Usage:
        .. code-block:: python
            :linenos:

            Scenario: Download as .docx
                Given I am logged in as manager
                And I have valid applications
                When I go to application_report
                Then I should receive a docx file download

    """
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


@then("I should see a success message")
def confirm_success_message(context):
    assert context.browser.find_by_css('.alert-success')


@then("I should( not)? see the text '(.*)'")
def assert_text_on_page(context, should_not, text_to_find):
    b = context.browser
    if should_not:
        assert not b.is_text_present(text_to_find), "Expected not to see %s but did" % text_to_find
    else:
        assert b.is_text_present(text_to_find), "Expected to see %s but didn't" % text_to_find