from django.template.defaultfilters import title
from toolkit.views import CCESearchView, mark_safe

from .forms import ActivityLogSearchForm, ActivityLogAdvancedSearchForm
from .models import ToolkitActivityLog


class ToolkitActivityLogListView(CCESearchView):
    template_name = "toolkit_activity_log/browse_activities.html"
    page_title = "Browse Activities"
    sidebar_group = ['dashboard']
    paginate_by = 20
    model = ToolkitActivityLog
    search_form_class = ActivityLogSearchForm
    advanced_search_form_class = ActivityLogAdvancedSearchForm
    ordering = ('-created_at', )
    columns = [
        ('Type', lambda a: mark_safe('<i class="%s"></i> %s' % (a.activity_type.logo, title(a.activity_type))),
         '', 'activity_type.activity_type'),
        ('Activity', 'summary', '2'),
        ('Description', 'description', '5'),
        ('User', lambda a: a.created_by.get_full_name() if a.created_by else '--', '2', 'created_by.first_name'),
        (
            'Date/Time',
            lambda a: mark_safe(
                '<span class="badge"><abbr class="timeago" title="%s"></abbr></span>' % a.created_at.isoformat()
            ), '', 'created_at'
        ),
    ]

    def render_buttons(self, user, obj, *args, **kwargs):
        return [self.render_button(btn_class='btn-info',
                                   label='View',
                                   icon_classes='glyphicon glyphicon-info-sign',
                                   url=obj.resolved_url)]

    def get_queryset(self):
        return super(ToolkitActivityLogListView, self).get_queryset().scoped_by_user(self.request.user)
