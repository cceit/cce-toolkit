from toolkit.helpers.reports import xlsx_response


class PlankReports(object):
    @classmethod
    def plank_creation_report(cls, qs, form):
        data = [[
            'Title',
            'Board',
            'Owner',
            'Created',
        ]]

        for planks in qs:
            row = [
                planks.title,
                planks.board.name,
                planks.owner.username,
                planks.created,
            ]
            data.append(row)

        return xlsx_response('plank_reports (xlsx)', data)
