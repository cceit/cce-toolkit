import os

from django.conf import settings
from django.core.management import call_command
from pyvirtualdisplay import Display
from splinter import Browser

from toolkit.helpers.utils import snakify


def setup_test_environment(context, scenario, visible=0, use_xvfb=True):
    """
    Method used to setup the BDD test environment
     - Sets up virtual display
     - Sets up webdriver instance
     - Sets window size
     - Flushes cookies
     - Enables debug (Allows for more verbose error screens)
     - Sets scenario
     - Truncates database tables

    Options:
     - visible (0 or 1) - Toggle Xephyr to view the Xvfb instance for limited debugging. 0: Off, 1: On.
     - use_xvfb (True/False) - Toggle Xvfb to run the tests on your desktop for in-depth debugging.
    """

    driver = os.environ.get('WEBDRIVER_TYPE', None)
    if driver == 'ie':

        webdriver_url = os.environ.get('WEBDRIVER_URL', None)
        if webdriver_url is None:
            raise EnvironmentError('WEBDRIVER_URL not set!')

        context.browser = Browser(
            driver_name="remote",
            url=webdriver_url,
            browser='internet explorer',
            platform="Windows 7",
            version="11",
            name="Remote IE Test"
        )

    else:  # Default Case
        if use_xvfb:
            context.display = Display(visible=visible, size=(1920, 1080))
            context.display.start()

        context.browser = Browser()

    context.browser.driver.set_window_size(1920, 1080)
    context.server_url = context.config.server_url
    # Flushes all cookies.
    context.browser.cookies.delete()
    # Re-enables yellow screens on failure. (Normally disabled by
    # LiveServerTestCase)
    settings.DEBUG = True
    context.scenario = scenario.name
    call_command('flush', verbosity=0, interactive=False)


def save_failure_screenshot(context, step):
    if step.status == "failed":
        file_path = '%s_%s_error.png' % (snakify(context.scenario), snakify(step.name))
        context.browser.driver.save_screenshot(file_path)


def flush_context(context, scenario):
    context.browser.quit()  # Close the browser to get a fresh one for each test
    context.browser = None  # Flush browser from context
    if hasattr(context, 'display'):
        context.display.stop()  # Closes the virtual display (if it exists)
