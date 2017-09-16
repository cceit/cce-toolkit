from django import template
from user_agents import parse

register = template.Library()


@register.filter
def simple_user_agent(value):
    user_agent = parse(value)
    return str(user_agent)
