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


def access_history_report():
    # PROTOTYPE access report which uses the apache log to generate data.
    # Really we want this to be generated from GA or similar.
    table = []
    context = {}

    year = datetime.now().year
    months = ["{}-{:0>2}-01".format(year, x) for x in range(12, 0, -1)]
    entries = defaultdict(list)

    with open(LOGFILE, 'r') as f:
        for line in f.readlines():
            dataset_name = line_is_dataset_view(line)
            if not dataset_name:
                continue

            pkg = toolkit.get_action('package_show')(context, {
                'id': dataset_name
            })

            # We should really regex this out of the line with the name ....
            parts = line.split(' ')
            entry_date = datetime.strptime(parts[3][1:], "%d/%b/%Y:%H:%M:%S")
            if entry_date.year != year:
                continue

            we = WorkingEntry()
            we.dataset_name = dataset_name
            we.organisation_name = pkg['organization']['name']
            we.organisation_title = pkg['organization']['title']
            we.date = entry_date.strftime("%Y-%m-01")

            entries[we.date].append(we)

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
            we = [1 for o in entries.get(month, []) if o.organisation_name == organisation['name']]
            totes = sum(we) or random.randint(0, 150)
            entry[month] = {'visited': totes, 'search': random.randint(0,500)}

        table.append(entry)

    return {
        'table': table
    }
