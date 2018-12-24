# A prototype report for showing the quality of the metadata that we have
# retrieved.  Currently this just gives every dataset a score of 100 and
# then removes points for bad metadata.  At present we only have a couple
# of criteria, but we can always add others in the rank_dataset function.
import json
from pprint import pprint

import ckan.plugins.toolkit as toolkit

from ckanext.defra.helpers import is_private_resource, get_resource_name


def _get_records(offset=0):
    return toolkit.get_action('package_search')({}, {
        'q': '',
        'rows': 10000,
        'start': offset
    })


def system_stats_report():
    # PROTOTYPE report that measures specific stats to allow us to make
    # decisions on the direction of the alpha
    counts = {
        'total_datasets': 0,
        'with_contact_email': 0,
        'with_maintainer_email': 0,
        'with_maintainer_name': 0,
        'licenses': {},
        'import_sources': {},
        'open_datasets': 0,
        'private_resources': 0,
        'resource_formats': {},
    }

    harvest_sources = toolkit.get_action('harvest_source_list')({}, {
        'all': True
    })

    # Load all datasets for processing
    response = _get_records(0)
    total_records = response['count']
    datasets = response['results']

    while len(datasets) != total_records:
        response = _get_records(len(datasets))
        datasets += response['results']

    for dataset in datasets:
        extras = {extra['key']: extra['value'] for extra in dataset['extras']}

        if extras.get('contact-email', None) not in [None, '']:
            counts['with_contact_email'] += 1

        if dataset.get('maintainer_email', None) not in [None, '']:
            counts['with_maintainer_email'] += 1

        if dataset.get('maintainer', None) not in [None, '']:
            counts['with_maintainer_name'] += 1

        license = dataset.get('license_id', '')
        if license is None:
            license = ''

        if license not in counts['licenses']:
            counts['licenses'][license] = 0
        counts['licenses'][license] += 1

        source = extras.get('import_source', '')
        if source.startswith('ONS'):
            source = 'ONS Test Data'
        elif source == '':
            source = 'Unknown'
        if source not in counts['import_sources']:
            counts['import_sources'][source] = 0
        counts['import_sources'][source] += 1

        if dataset.get('is_open', False):
            counts['open_datasets'] += 1

        if is_private_resource(dataset):
            counts['private_resources'] += 1

        for resource in dataset['resources']:
            if resource['format'] not in counts['resource_formats']:
                counts['resource_formats'][resource['format']] = 0
            counts['resource_formats'][resource['format']] += 1

        counts['total_datasets'] += 1

    return {
        'table': [''],
        'are_some_results': True,
        'counts': counts,
        'harvest_sources': harvest_sources,
    }
