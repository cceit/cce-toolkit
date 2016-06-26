from django import template

register = template.Library()


@register.inclusion_tag("breadcrumbs.html", takes_context=True)
def breadcrumbs(context):
    """
    Tag renders breadcrumb in template
    """
    if "breadcrumbs" in context.dicts[1]:
        return {"breadcrumbs": context.dicts[1]["breadcrumbs"]}
    else:
        return {"breadcrumbs": []}
