from collections import OrderedDict

from django.template.defaultfilters import title
from user_agents import parse

from toolkit.views import ReportDownloadSearchView, mark_safe
from .forms import ActivityLogAdvancedSearchForm, ActivityLogSearchForm
from .models import ToolkitActivityLog


class ToolkitActivityLogListView(ReportDownloadSearchView):
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
        ('Description', 'description'),
        ('User Agent', lambda a: str(parse(a.user_agent)) if a.user_agent else '--', '2', 'user_agent'),
        ('IP Address', lambda a: a.ip_address if a.ip_address else '--', '1', 'ip_address'),
        ('User', lambda a: a.created_by if a.created_by else '--', '2', 'created_by'),
        (
            'Created',
            lambda a: mark_safe(
                '<time class="timeago pull-right" datetime="%s" title="%s">%s</time>' % (
                    a.created_at.isoformat(),
                    a.created_at.strftime('%m/%d/%Y %I:%M%p'),
                    a.created_at.strftime('%m/%d/%Y')
                )
            ), '', 'created_at'
        ),
    ]

    def render_buttons(self, user, obj, *args, **kwargs):
        return [
            self.render_button(
                btn_class='btn-info',
                label='View',
                icon_classes='glyphicon glyphicon-info-sign',
                url=obj.resolved_url
            ),
        ]

    def get_reports(self):
        reports = OrderedDict()
        reports.update({
            'activity_xlsx_report': {'name': 'Activity Report (XLSX)', 'method': 'activity_xlsx_report'},
        })
        return reports

    def get_queryset(self):
        # This repeats the functionality of ActivitiesPermissionManager.scoped_by_user().
        return super(ToolkitActivityLogListView, self).get_queryset().for_user(self.request.user)

