import uuid

from django.core.management import call_command
from toolkit.helpers.bdd import setup_test_environment
from toolkit.helpers.utils import snakify


# The scenario param is used behind the scenes
def before_scenario(context, scenario):
    setup_test_environment(context, scenario)
    call_command('loaddata', 'auth.json')


def after_step(context, step):
    # Take a screenshot if the step failed
    if step.status == "failed":
        file_path = '%s_%s_%s.png' % (snakify(context.scenario),
                                      snakify(step.name),
                                      uuid.uuid4())
        context.browser.driver.save_screenshot(file_path)


def after_scenario(context, scenario):
    call_command('flush', verbosity=0, interactive=False)

    # Close the browser to get a fresh one for each test
    context.browser.quit()

    context.browser = None  # Flush browser from context

    context.display.stop()  # Closes the virtual display
