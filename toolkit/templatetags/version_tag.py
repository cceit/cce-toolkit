import time

from django import template
from django.conf import settings
from django.templatetags.static import StaticNode
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def versioning_string():
    """
    Helper method for versioning javascript and other static files.
    It returns WEBSITE_VERSION on the live site, where files should only change when the version does,
    while it returns a ms time string when debug is on, so that UAT's files never get cached by the browser
    """

    if settings.DEBUG:
        return int(time.time())
    elif hasattr(settings, 'WEBSITE_VERSION'):
        return settings.WEBSITE_VERSION
    else:
        return "default"


class VersionStaticNode(StaticNode):
    def render(self, context):
        url = self.url(context)
        version = versioning_string()
        out_str = format_html("{}?version={}", url, versioning_string())
        if self.varname is None:
            return out_str
        context[self.varname] = out_str
        return ''


@register.tag('v_static')
def do_version_static(parser, token):
    return VersionStaticNode.handle_token(parser, token)
