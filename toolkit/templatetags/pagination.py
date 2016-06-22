from django import template
from django.utils.safestring import mark_safe

register = template.Library()


# http://stackoverflow.com/a/16609498/1233289
@register.simple_tag
def url_replace(request, value):
    dict_ = request.GET.copy()
    dict_['page'] = value
    return dict_.urlencode()


@register.simple_tag
def generate_ordering_links(request, title, value):
    if value:
        dict_ = request.GET.copy()
        dict_['page'] = 1
        order = ''
        icon = '<i class="fa fa-sort" aria-hidden="true"></i>'
        if 'order_by' in dict_ and dict_['order_by']:
            if value in dict_['order_by']:
                if dict_['order_by'][0] == '-':
                    order = ''
                    icon = '<i class="fa fa-sort-alpha-desc" aria-hidden="true"></i>'
                else:
                    order = '-'
                    icon = '<i class="fa fa-sort-alpha-asc" aria-hidden="true"></i>'

        dict_['order_by'] = '%s%s' % (order, value)
        return mark_safe('<a href="?%s" style="white-space: nowrap">%s %s</a>' % (dict_.urlencode(), icon, title))
    else:
        return title


@register.simple_tag
def append_querystrings_as_hidden_fields(request):
    dict_ = request.GET.copy()
    hidden_fields = []
    for k, v in dict_.items():
        hidden_fields.append('<input type="hidden" name="%s" value="%s">' % (k, v))
    return mark_safe(''.join(hidden_fields))


@register.simple_tag
def generate_page_links(page_obj, request):
    value = int(request.GET['page']) if 'page' in request.GET else 1
    links = []
    if page_obj.has_previous():
        links.append('<li class="arrow"><a href="?%s" class="page" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % url_replace(request, page_obj.previous_page_number()))

    links.append('<li class="page %s"><a href="?%s" class="">1</a></li>' % ('active' if value == 1 else '', url_replace(request, 1)))
    for x in range(value - 7, value + 7):
        if 1 < x < page_obj.paginator.num_pages:
            url = url_replace(request, x)
            if x == value:
                links.append('<li class="active"><a href="?%s" class="page">%s</a></li>' % (url, x))
            else:
                links.append('<li><a href="?%s" class="page">%s</a></li>' % (url, x))

    links.append(
        '<li class="page %s"><a href="?%s">%s</a></li>' % ('active' if value == page_obj.paginator.num_pages else '',
                                                           url_replace(request, page_obj.paginator.num_pages),

                                                           page_obj.paginator.num_pages))
    if page_obj.has_next():
        links.append('<li class="arrow"><a href="?%s" class="page" aria-label="Next"><span aria-hiddent="true">&raquo;</span></a></li>' % url_replace(request, page_obj.next_page_number()))

    return mark_safe("".join(links))
