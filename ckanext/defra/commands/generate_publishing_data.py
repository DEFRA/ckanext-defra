from collections import Counter
from datetime import datetime

import ckan.plugins.toolkit as toolkit


class GeneratePublishingDataCommand(toolkit.CkanCommand):
    ''' Generates data for publishing report as a Python file for use as
        a prototype. For the actual solution, it's likely a better way
        will be required to store this data. Maybe via
        https://github.com/datagovuk/ckanext-report '''

    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0

    def get_context(self):
        return {
            'ignore_auth': True,
        }

    def header(self):
        print "PUBLISHING_HISTORY = {"

    def footer(self):
        print "}"

    def _is_in_range(self, num):
        return num > 2011 and num <= datetime.now().year

    def modification_list(self, datasets):
        c = Counter()

        for dataset in datasets:
            date = datetime.strptime(dataset['metadata_modified'], '%Y-%m-%dT%H:%M:%S.%f')
            if date.year == 2018 and dataset['metadata_modified'] != dataset['metadata_created']:
                c[date.month] += 1

        return ['"Updated records"'] + [str(c[x]) for x in range(1, 13)]

    def addition_list(self, datasets):
        c = Counter()

        for dataset in datasets:
            date = datetime.strptime(dataset['metadata_created'], '%Y-%m-%dT%H:%M:%S.%f')
            if date.year == 2018:
                c[date.month] += 1

        return ['"New records"'] + [str(c[x]) for x in range(1, 13)]

    def entry(self, organisation, datasets):
        print '    "{}": {{'.format(organisation['name'])
        print '        "updates": [{}],'.format(', '.join(self.modification_list(datasets)))
        print '        "additions": [{}]'.format(', '.join(self.addition_list(datasets)))
        print '    },'

    def command(self):
        self._load_config()
        self.header()

        organisation_list = toolkit.get_action('organization_list')(
            self.get_context(), {
                'all_fields': True,
            }
        )

        for organisation in organisation_list:
            datasets = toolkit.get_action('package_search')(
                self.get_context(), {
                    'q': 'owner_org:{}'.format(organisation['id']),
                    'rows': 10000
                }
            )['results']

            self.entry(organisation, datasets)

        self.footer()
