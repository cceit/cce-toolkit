import datetime


# Logs to JS console, since Behave won't let us use Python's print
def log(context, text):
    script_text = 'console.log("%s")' % text
    context.browser.execute_script(script_text)


def fill_and_submit_form(browser, fields, submit_button_name='submit'):
    for field in fields:
        function = field['function']
        name = field['name']
        if 'value' in field:
            value = field['value']
            getattr(browser, function)(name, value)
        else:
            getattr(browser, function)(name)
    browser.find_by_name(submit_button_name).first.click()


def assert_text_on_page(browser, fields,  date_format='%m/%d/%Y'):
    for field in fields:
        text = field.strftime(date_format) if isinstance(field, datetime.date) else '%s' % field
        assert browser.is_text_present(text), "Could not find '%s' on the page" % text


def assert_text_in_table(browser, fields, date_format='%m/%d/%Y'):
    rows = browser.find_by_css('tr')
    contains_test_obj = False

    failing_field = None
    for row in rows:
        for field in fields:
            field = field.strftime(date_format) if isinstance(field, datetime.date) else '%s' % field
            if field in row.text:
                continue
            else:
                failing_field = field
                break
        else:
            contains_test_obj = True
            break

    assert contains_test_obj, "Couldn't find the test row in the table%s" % (
        ': ' + failing_field if failing_field else '')


def set_test_obj_pk(context):
    if hasattr(context, 'test_obj'):
            context.test_obj_pk = context.test_obj.pk


def set_test_obj(context, model):
    if hasattr(context, 'test_obj_pk'):
        context.test_obj = model.objects.get(pk=context.test_obj_pk)
    else:
        context.test_obj = model.objects.all().order_by('-pk').first()


def get_file_content_type(file_type):

    try:
        file_types = {
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'xls': 'application/vnd.ms-excel',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'pdf': 'application/pdf',
        }
    except KeyError:
        return NotImplementedError

    return file_types[file_type]

