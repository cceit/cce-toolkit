import datetime

import requests
from requests.exceptions import MissingSchema
from splinter.exceptions import ElementDoesNotExist


def click_element_by_name(browser, name, index=0):
    """
    Clicks an element in the DOM by the element name

    :param browser: browser object
    :param string name: name of element
    :param integer index: index of the element in the DOM
    """
    browser.find_by_name(name)[index].click()


def fill_form(browser, fields):
    """
    Fills a dictionary of form fields on a page

    :param browser: browser object
    :param fields: iterable of fields
    """
    for field in fields:
        function = field['function']
        name = field['name']
        if 'value' in field:
            value = field['value']
            getattr(browser, function)(name, value)
        else:
            getattr(browser, function)(name)


def fill_and_submit_form(browser, fields, submit_button_name='submit'):
    """
    Fills a dictionary of form fields on a page and clicks the submit button

    :param browser: browser object
    :param fields: iterable of fields
    :param string submit_button_name: optional button name field in case
     there's multiple buttons on the page
    """
    fill_form(browser, fields)
    click_element_by_name(browser, submit_button_name)


def assert_text_in_table(browser, values, date_format='%m/%d/%Y'):
    """
    Asserts that a list of values exists in table rows on the page

    :param browser: browser object
    :param list values: list of values
    :param string date_format: optional field to specify a specific string
     format for date values sent in the values list
    """
    rows = browser.find_by_css('tr')
    contains_test_obj = False
    failing_value = None

    for row in rows:
        if contains_test_obj:
            break
        for value in values:
            value = value.strftime(date_format) \
                if isinstance(value, datetime.date) else '%s' % value

            if value in row.text:
                contains_test_obj = True
                failing_value = value
                break

    assert contains_test_obj, "Couldn't find the test row in the table%s" % (
        ': ' + failing_value if failing_value else ''
    )


def assert_text_not_in_table(browser, values, date_format='%m/%d/%Y'):
    """
    Asserts that a list of values does not exist in table rows on the page

    :param browser: browser object
    :param list values: list of values
    :param string date_format: optional field to specify a specific string
     format for date values sent in the values list
    """
    rows = browser.find_by_css('tr')
    contains_test_obj = False
    failing_value = None

    for row in rows:
        if contains_test_obj:
            break
        for value in values:
            value = value.strftime(date_format) \
                if isinstance(value, datetime.date) else '%s' % value
            if value in row.text:
                contains_test_obj = True
                failing_value = value
                break

    assert not contains_test_obj, "Found unexpected row in the table%s" % (
        ': ' + failing_value if failing_value else ''
    )


def get_file_content_type(extension):
    """
    :param string extension: file extension

    :returns string: mime type based on file extension
    """
    try:
        mime_types = {
            'docx': 'application/vnd.openxmlformats-officedocument'
                    '.wordprocessingml.document',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument'
                    '.spreadsheetml.sheet',
            'pdf': 'application/pdf',
            'csv': 'text/csv',
        }
    except KeyError:
        return NotImplementedError

    return mime_types[extension]


def scroll_to_top(browser):
    """
    executes the following js code on the page: window.scrollTo(0, 0)
    """
    browser.driver.execute_script("window.scrollTo(0, 0);")


def compare_content_types(browser, context, file_type):
    """
    Attempts to find the download link, request the file and asserts that
    the file extension matches the expected file type
    """

    if hasattr(context, 'file_url'):  # Should be deprecated for context.url soon
        request = requests.get(context.file_url, cookies=browser.cookies.all())
    elif hasattr(context, 'result'):
        request = context.result
    else:
        try:
            file_url = browser.find_by_name('download').first['href']
            request = requests.get(file_url, cookies=browser.cookies.all())
        except (ElementDoesNotExist, MissingSchema):
            request = requests.get(context.url, cookies=browser.cookies.all())

    target_type = get_file_content_type(file_type)
    received_type = request.headers['content-type']

    return target_type, received_type


def log(context, text):
    """
    logs text in the js console
    """
    script_text = 'console.log("%s")' % text
    context.browser.execute_script(script_text)


def assert_text_on_page(browser, values, date_format='%m/%d/%Y'):
    """
    Asserts that a list of values does exist on the page

    :param browser: browser object
    :param list values: list of values
    :param string date_format: optional field to specify a specific string
     format for date values sent in the values list
    """
    for value in values:
        text = value.strftime(date_format) \
            if isinstance(value, datetime.date) else '%s' % value
        assert browser.is_text_present(text), \
            "Could not find '%s' on the page" % text


def set_test_obj_pk(context):
    """
    Sets the test object pk
    """
    if hasattr(context, 'test_obj'):
            context.test_obj_pk = context.test_obj.pk


def set_test_obj(context, model):
    """
    Sets the test object
    """
    if hasattr(context, 'test_obj_pk'):
        context.test_obj = model.objects.get(pk=context.test_obj_pk)
    else:
        context.test_obj = model.objects.all().order_by('-pk').first()
