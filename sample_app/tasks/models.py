from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from toolkit.models import CCEAuditModel

from boards.models import Board
from tasks.reports import TaskReports


class Task(CCEAuditModel):
    STARTED = 'started'
    PENDING = 'pending'
    COMPLETE = 'complete'
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (STARTED, 'Started'),
        (COMPLETE, 'Complete'),
    )
    title = models.CharField(max_length=200)
    description = models.CharField(blank=True, max_length=200)
    image = models.ImageField(upload_to='task_images', blank=True, null=True)
    attachment = models.FileField(upload_to='task_attachment', blank=True,
                                  null=True)
    board = models.ForeignKey(Board, related_name='tasks')
    completed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=128, choices=STATUS_CHOICES,
                              blank=True,
                              default=PENDING)
    reports = TaskReports()

    def __str__(self):
        return u'/t/%s' % self.title

    def get_absolute_url(self):
        return reverse('view_task', kwargs={'pk': self.pk})

    def get_status_update_url(self):
        return reverse('update_task_status', kwargs={'pk': self.pk})

    def is_owner(self, user_obj):
        return user_obj == self.created_by

    def can_update(self, user_obj):
        return True

    def can_delete(self, user_obj):
        return self.created_by == user_obj or user_obj.is_staff

    def can_create(self, user_obj):
        return True

    def can_view_list(self, user_obj):
        return True

    def can_view(self, user_obj):
        return True
