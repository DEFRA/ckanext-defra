from collections import defaultdict
from datetime import datetime
import random

import ckan.plugins.toolkit as toolkit


def publishing_history_report():
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
        datasets = toolkit.get_action('package_search')(
            context, {
                'q': 'owner_org:{}'.format(organisation['id']),
                'rows': 10000
            }
        )['results']

        entry = {
            'name': organisation['name'],
            'title': organisation['title'],
        }

        def new_inner_dict():
            return {'added': random.randint(1, 20), 'modified': random.randint(5, 50)}

        values = defaultdict(new_inner_dict)
        for dataset in datasets:
            date = datetime.strptime(dataset['metadata_created'], '%Y-%m-%dT%H:%M:%S.%f')
            partial = "{}-{:0>2}-01".format(date.year, date.month)
            values[partial]['added'] = values[partial]['added'] + 1

            date = datetime.strptime(dataset['metadata_modified'], '%Y-%m-%dT%H:%M:%S.%f')
            partial = "{}-{:0>2}-01".format(date.year, date.month)
            values[partial]['modified'] = values[partial]['modified'] + 1

        for month in months:
            entry[month] = values[month]

        table.append(entry)

    return {
        'table': table
    }
