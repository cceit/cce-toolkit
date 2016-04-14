from django.conf import settings
from pyvirtualdisplay import Display
from splinter import Browser


def setup_test_environment(context, scenario):
    context.display = Display(visible=0, size=(1920, 1080))  # Our virtual display to run firefox
    context.display.start()
    context.browser = Browser()  # This is our base webdriver instance. It uses Firefox by default.
    context.browser.driver.set_window_size(1920, 1080)
    context.server_url = 'http://localhost:%s' % settings.TEST_PORT
    context.browser.cookies.delete()  # Flushes all cookies.
    settings.DEBUG = True  # Re-enables yellow screens on failure. (Normally disabled by LiveServerTestCase)
    context.scenario = scenario.name
