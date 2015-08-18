from django import template
from django.conf import settings

register = template.Library()


@register.assignment_tag
def collect_issues():
    return settings.COLLECT_ISSUES


