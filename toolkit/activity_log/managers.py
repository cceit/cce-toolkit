# from django.contrib.contenttypes.models import ContentType
# from django.db import models
# from django.db.models import Q
#
# from employees.models import Employee
# from leave.models import LeaveRequest
# from positions.models import Position
# from timesheets.models import MonthlyTimesheet, HourlyTimesheet, ACATimesheet
# from roles.models import Roles, UserMeta
#
#
# class ActivityLogPermissionManager(models.Manager):
#     def scoped_by(self, user_obj):
#
#         monthly_timesheets = MonthlyTimesheet.objects.filter(Q(position__pk__in=Position.accessible_pks(user_obj)))\
#             .distinct()
#
#         hourly_timesheets = HourlyTimesheet.objects.filter(Q(position__pk__in=Position.accessible_pks(user_obj)))\
#             .distinct()
#
#         aca_timesheets = ACATimesheet.objects.filter(Q(position__pk__in=Position.accessible_pks(user_obj)))\
#             .distinct()
#         leave_requests = LeaveRequest.objects.filter(Q(position__pk__in=Position.accessible_pks(user_obj))).distinct()
#         positions = Position.objects.filter(Q(pk__in=Position.accessible_pks(user_obj))).distinct()
#         employees = Employee.objects.filter(pk__in=Employee.accessible_pks(user_obj)).distinct()
#         if Roles.is_administrator(user_obj):
#             usermetas = UserMeta.objects.all()
#         else:
#             usermetas = UserMeta.objects.none()
#
#         return self.filter(
#             Q(
#                 object_id__in=monthly_timesheets.values('id'),
#                 content_type=ContentType.objects.get_for_model(MonthlyTimesheet)
#             ) |
#             Q(
#                 object_id__in=aca_timesheets.values('id'),
#                 content_type=ContentType.objects.get_for_model(ACATimesheet)
#             ) |
#             Q(
#                 object_id__in=hourly_timesheets.values('id'),
#                 content_type=ContentType.objects.get_for_model(HourlyTimesheet)
#             ) |
#             Q(
#                 object_id__in=leave_requests.values('id'),
#                 content_type=ContentType.objects.get_for_model(LeaveRequest)
#             ) |
#             Q(
#                 object_id__in=positions.values('id'),
#                 content_type=ContentType.objects.get_for_model(Position)
#             ) |
#             Q(
#                 object_id__in=employees.values('id'),
#                 content_type=ContentType.objects.get_for_model(Employee)
#             ) |
#             Q(
#                 object_id__in=usermetas.values('id'),
#                 content_type=ContentType.objects.get_for_model(UserMeta)
#             )
#         )
