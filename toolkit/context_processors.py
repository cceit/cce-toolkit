from django.conf import settings
from django.contrib.sites.models import Site


def export_site_object(request):
    context = {}
    try:
        site_obj = Site.objects.get(pk=settings.SITE_ID)

        context.update({"site_domain": site_obj.domain,
                        "site_name": site_obj.name})

    except Site.DoesNotExist:
        pass

    return context
