import json
import sys

import ckan.plugins.toolkit as toolkit

from import_publishers import PublisherStub, PUBLISHERS

CLEAN_LIST = [
    'relationships_as_object',
    'unpublished',
    'num_tags',
    'num_resources',
    'revision_id',
    'revision_timestamp',
    'groups',
    'isopen',
    'organization',
    'metadata_created',
    'metadata_modified',
    'relationships_as_object',
    'relationships_as_subject',
    'tracking_summary',
    'theme-primary',
    'theme-secondary',
    'extras',
    'archiver',
    'individual_resources',
    'additional_resources',
    'timeseries_resources',
    'resources',
    'qa'
]

class ImportDataCommand(toolkit.CkanCommand):
    ''' Imports datasets from data.gov.uk for our organisations'''
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0

    def get_context(self):
        return {
            'ignore_auth': True,
        }

    def clean_resource(self, r):
        for k in ['archiver', 'qa', 'revision_id', 'tracking_summary']:
            if k in r:
                del r[k]
        return r

    def clean_extra(self, extra):
        return {'key': extra['key'], 'value': extra['value']}

    def clean(self, dataset):
        old_extras = dataset['extras'][:]
        old_resources = dataset['resources'][:]
        old_tags = dataset['tags'][:]

        for k in CLEAN_LIST:
            if k in dataset:
                del dataset[k]

        dataset['extras'] = []
        for extra in old_extras:
            dataset['extras'].append(self.clean_extra(extra))

        dataset['resources'] = []
        for resource in old_resources:
            dataset['resources'].append(self.clean_resource(resource))

        dataset['tags'] = []
        for tag in old_tags:
            del tag['revision_timestamp']
            del tag['id']
            dataset['tags'].append(tag)

    def save_dataset(self, dataset):
        try:
            toolkit.get_action('package_create')(
                self.get_context(), dataset
            )
            return 1
        except:
            print "{} already exists".format(dataset['id'])
        return 0

    def command(self):
        self._load_config()

        publisher_lookup = {}
        dgu_lookup = {}

        for p in PUBLISHERS:
            if p.dgu_name == '':
                continue
            dgu_lookup[p.name] = p.dgu_name


        existing_publishers = toolkit.get_action('organization_list')(
            self.get_context(), {'all_fields': True}
        )
        for publisher in existing_publishers:
            dgu_name = dgu_lookup.get(publisher['name'])
            if not dgu_name:
                continue

            publisher_lookup[dgu_name] = publisher['id']

        counter = 0
        for row in open('datasets.jsonl', 'r').readlines():
            dataset = json.loads(row)
            org_name = dataset['organization']['name']
            if not org_name in publisher_lookup:
                continue


            dataset['owner_org'] = publisher_lookup[org_name]
            self.clean(dataset)
            counter += self.save_dataset(dataset)

        print "Imported {} datasets".format(counter)
