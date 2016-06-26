from django.conf import settings
from pyvirtualdisplay import Display
from splinter import Browser


def setup_test_environment(context, scenario):
    """
    Method used to setup the BDD test environment
     - Sets up Virtual Display
     - Sets up Browser
     - Sets window size
     - flushes cookies
     - Turn on debug(useful when capturing screenshots of the errors)
     - Sets Scenario


    """
    # Our virtual display to run firefox
    context.display = Display(visible=0, size=(1920, 1080))
    context.display.start()
    # This is our base webdriver instance. It uses Firefox by default.
    context.browser = Browser()
    context.browser.driver.set_window_size(1920, 1080)
    context.server_url = 'http://localhost:%s' % settings.TEST_PORT
    # Flushes all cookies.
    context.browser.cookies.delete()
    # Re-enables yellow screens on failure. (Normally disabled by
    # LiveServerTestCase)
    settings.DEBUG = True
    context.scenario = scenario.name
