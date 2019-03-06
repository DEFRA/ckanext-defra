import json
import os

import ckan.plugins.toolkit as toolkit
from ckan.logic import NotFound


class ImportPublishersCommand(toolkit.CkanCommand):
    """
    Imports all of the publishers for Defra (inc. defra) '''
    """
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0
    context = {
        'ignore_auth': True
    }

    def command(self):
        fixture = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'fixtures', 'publishers.json'
        )
        self._load_config()

        with open(fixture, 'r') as fh:
            publishers = json.loads(fh.read())

        add_count = 0
        update_count = 0

        existing_harvesters = {
            x['url']: x for x in toolkit.get_action('harvest_source_list')(self.context, {})
        }

        for publisher in publishers:
            pub_dict = {
                'name': publisher['name'],
                'title': publisher['title'],
                'image_url': publisher['image_url'],
                'extras': [],
            }

            if len(publisher['contacts']) > 0:
                pub_dict['extras'].append({
                    'key': 'contact_emails',
                    'value': ','.join(publisher['contacts'])
                })

            action = 'organization_create'
            if self._publisher_exists(publisher):
                action = 'organization_update'
                pub_dict['id'] = publisher['name']
                update_count += 1
            else:
                add_count += 1

            saved = toolkit.get_action(action)(self.context, pub_dict)

            for harvester in publisher['harvesters']:
                harvest_dict = {
                    'name': harvester['name'],
                    'title': harvester['title'],
                    'url': harvester['url'],
                    'source_type': harvester['source_type'],
                    'owner_org': saved['id'],
                    'frequency': 'WEEKLY',
                }

                harvest_action = 'harvest_source_create'
                if harvester['url'] in existing_harvesters:
                    harvest_action = 'harvest_source_update'
                    harvest_dict['id'] = existing_harvesters[harvester['url']]['id']

                toolkit.get_action(harvest_action)(self.context, harvest_dict)

        print('Created {} and updated {} publishers'.format(add_count, update_count))

    def _publisher_exists(self, publisher):
        try:
            toolkit.get_action('organization_list')(
                self.context,
                {'id': publisher['name']}
            )
        except NotFound:
            return False
        return True

