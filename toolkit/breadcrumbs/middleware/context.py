from django.core.urlresolvers import resolve
from django.http import Http404


def get_class(c):
    parts = c.split('.')
    module = ".".join(parts[:-1])
    m = __import__(module)
    for comp in parts[1:]:
        m = getattr(m, comp)
    return m


def update_breadcrumb(url, breadcrumbs):
    func, args, kwargs = resolve(url)
    clss = get_class('{0}.{1}'.format(func.__module__, func.__name__))

    if 'extra_context' in kwargs and 'breadcrumb_name' \
            in kwargs['extra_context']:
        breadcrumbs.append((kwargs['extra_context']['breadcrumb_name'], url))
    else:
        try:
            page = clss(kwargs=kwargs)
            breadcrumbs.append((page.get_page_title, url))
        except (AttributeError, TypeError), e:
            pass


def process_context(req):
    tokens = req.path.split("/")
    subpaths = ["/" + "/".join(tokens[1:n + 1])
                for n in range(len(tokens[:-1]))]
    breadcrumbs = []

    for u in subpaths:
        try:
            update_breadcrumb(u, breadcrumbs)
        except Http404:
            try:
                update_breadcrumb(u + "/", breadcrumbs)
            except Http404:
                pass
            except AttributeError:
                pass

    return {"breadcrumbs": breadcrumbs}
