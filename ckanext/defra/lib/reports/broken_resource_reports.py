from collections import defaultdict
from datetime import datetime
import random
import re

import ckan.plugins.toolkit as toolkit

LOGFILE = "/var/log/apache2/ckan_default.custom.log"
DATASETNAME_REGEX = re.compile(".*GET /dataset/([a-z0-9\-]+).*")


def line_is_dataset_view(line):
    m = DATASETNAME_REGEX.match(line)
    if not m:
        return None

    return m.groups()[0]


class WorkingEntry(object):
    organisation_name = ""
    organisation_title = ""
    date = None
    dataset_name = ""


def broken_resource_report():
    table = []
    context = {}

    year = datetime.now().year
    months = ["{}-{:0>2}-01".format(year, x) for x in range(12, 0, -1)]

    organisation_list = toolkit.get_action('organization_list')(
        context, {
            'all_fields': True,
            'include_datasets': True
        }
    )

    for organisation in organisation_list:
        entry = {
            'name': organisation['name'],
            'title': organisation['title'],
        }

        for month in months:
            entry[month] = {'broken': random.randint(0, 30)}

        table.append(entry)

    return {'table': table}