from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from toolkit.models import CCEAuditModel, CCEModel

from .managers import ActivityTypePermissionManager


class ActivityType(CCEModel):
    activity_type = models.CharField(max_length=64)
    logo = models.CharField(max_length=128, blank=True)
    groups = models.ManyToManyField(to=Group)
    include_creator = models.BooleanField(default=True)
    permissions = ActivityTypePermissionManager()
    objects = models.Manager()

    class Meta:
        db_table = 'cce_toolkit_activity_types'
        ordering = ('activity_type',)

    def __unicode__(self):
        return self.activity_type

    def can_view_list(self, user_obj):
        return True

    def can_create(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True

    def can_update(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return True


class ActivityLog(CCEAuditModel):
    summary = models.TextField(max_length=128)
    description = models.TextField(max_length=256)
    activity_type = models.ForeignKey(ActivityType)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    absolute_url_name = models.CharField(max_length=64, blank=True)

    class Meta:
        db_table = 'cce_toolkit_activity_log'
        ordering = ('-pk',)

    def __unicode__(self):
        return "%s, %s - %s" % (self.created_at.strftime("%m/%d/%Y %I:%M"),
                                self.activity_type, self.summary)

    @property
    def icon_class(self):
        return self.ACTIVITY_ICONS[str(self.activity_type)]

    @classmethod
    def create_log(cls, summary, description, activity_type,
                   content_type_model, object_id, absolute_url_name=None):
        """

        :param string summary: Summary of the activity
        :param string description: Description of the activity
        :param instance activity_type: Activity Type object
        :param string content_type_model: Content Type of the model associated
         with the activity
        :param int/string object_id: The primary key of the object associated
         with the activity
        :param string absolute_url_name: The absolute url name of the object
         associated with the activity

        :returns: newly created activity log instance
        """
        log_obj = cls.objects.create(
            summary=summary,
            description=description,
            activity_type=activity_type,
            content_type=ContentType.objects.get_for_model(content_type_model),
            object_id=object_id,
        )

        if absolute_url_name is not None:
            log_obj.absolute_url_name = absolute_url_name
            log_obj.save()
        return log_obj

    def can_view_list(self, user_obj):
        return True

    def can_create(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True

    def can_update(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return True


