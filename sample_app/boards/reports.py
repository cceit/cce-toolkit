from toolkit.helpers.reports import xlsx_response


class BoardsReports(object):
    @classmethod
    def board_creation_report(cls, qs, form):
        data = [[
            'Name',
            'Description',
            'Creation Date',
        ]]

        for boards in qs:
            row = [
                boards.name,
                boards.description,
                boards.created,
            ]
            data.append(row)

        return xlsx_response('board_reports (xlsx)', data)
