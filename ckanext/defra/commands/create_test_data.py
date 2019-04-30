import json
import os

import ckan.plugins.toolkit as toolkit


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
    'archiver',
    'individual_resources',
    'additional_resources',
    'timeseries_resources',
    'resources',
    'qa'
]


class DefraCreateTestDataCommand(toolkit.CkanCommand):
    """
    Load feature test data
    """
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0

    def get_context(self):
        return {
            'ignore_auth': True
        }

    def command(self):
        fixture = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'fixtures', 'datasets.json'
        )
        self._load_config()

        with open(fixture, 'r') as fh:
            datasets = json.loads(fh.read())

        for dataset in datasets:
            resources = dataset['resources'][:]

            for k in CLEAN_LIST:
                if k in dataset:
                    del dataset[k]

            dataset['resources'] = []
            for resource in resources:
                for field in ['archiver', 'qa', 'revision_id', 'tracking_summary']:
                    if field in resource:
                        del resource[field]
                dataset['resources'].append(resource)

            try:
                toolkit.get_action('package_create')(
                    self.get_context(), dataset
                )
            except Exception, ex:
                print('ERROR: {} - {}'.format(dataset['name'], ex))
