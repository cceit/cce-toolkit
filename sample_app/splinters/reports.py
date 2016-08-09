from toolkit.helpers.reports import xlsx_response


class SplinterReports(object):
    @classmethod
    def splinter_creation_report(cls, qs, form):
        data = [[
            'Owner',
            'Plank',
            'Comment',
        ]]

        for splinters in qs:
            row = [
                splinters.owner.username,
                splinters.plank.title,
                splinters.comment,
            ]
            data.append(row)

        return xlsx_response('plank_reports (xlsx)', data)