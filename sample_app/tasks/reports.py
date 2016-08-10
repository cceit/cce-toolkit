from toolkit.helpers.reports import xlsx_response, generate_table


class TaskReports(object):
    @classmethod
    def task_report(cls, qs, form):
        data = [[
            'Title',
            'status',
            'Board',
            'Created By',
            'Created At',
        ]]

        for tasks in qs:
            row = [
                tasks.title,
                tasks.status,
                tasks.board.name,
                tasks.created_by.get_full_name(),
                tasks.created_at,
            ]
            data.append(row)

        return xlsx_response('task_report', data)

    @classmethod
    def detailed_task_report(cls, qs, form):
        columns = [
            ('Title', 'title'),
            ('Description', 'description'),
            ('Board', 'board__name'),
            ('Status', 'status'),
            ('Completed At', 'completed_at'),
            ('Created At', 'created_at'),
            ('Image', lambda obj: '%s' % obj.image.url),
            ('Attachment', lambda obj: 'X' if obj.attachment else ''),
        ]
        data = generate_table(columns=columns,
                              data=qs,
                              suppress_attr_errors=True)

        return xlsx_response('detail_tasks_report', data)
