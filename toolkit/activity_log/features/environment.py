from django.core.management import call_command
from toolkit.bdd.utils import setup_test_environment
from toolkit.utils import snakify


def before_scenario(context, scenario):  # The scenario param is used behind the scenes
    setup_test_environment(context, scenario)
    call_command('flush', verbosity=0, interactive=False)


def after_step(context, step):
    if step.status == "failed":
        file_path = '%s_%s.png' % (snakify(context.scenario), snakify(step.name))
        context.browser.driver.save_screenshot(file_path)


def after_scenario(context, scenario):
    context.browser.quit()  # Close the browser to get a fresh one for each test
    context.browser = None  # Flush browser from context
    context.display.stop()  # Closes the virtual display
