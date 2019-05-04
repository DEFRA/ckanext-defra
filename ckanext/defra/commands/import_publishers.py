import json
import os
import uuid

import ckan.plugins.toolkit as toolkit
from ckan.logic.action.create import NotFound
from ckan.logic import ValidationError


class ImportPublishersCommand(toolkit.CkanCommand):
    """
    Imports all of the publishers for Defra (inc. defra)
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
            os.path.dirname(os.path.dirname(__file__)), 'fixtures', 'publishers.json'
        )
        self._load_config()

        with open(fixture, 'r') as fh:
            publishers = json.loads(fh.read())

        saved_publishers = []
        saved_harvesters = []
        counts = {
            'add': 0,
            'update': 0,
            'delete': 0,
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

            publisher_id = self._get_publisher_id(publisher['name'])
            if publisher_id is None:
                action = 'organization_create'
                pub_dict['id'] = str(uuid.uuid4())
                counts['add'] += 1
            else:
                pub_dict['id'] = publisher_id
                action = 'organization_update'
                counts['update'] += 1

            saved_publisher = toolkit.get_action(action)(
                self.get_context(), pub_dict
            )
            saved_publishers.append(saved_publisher['id'])

            for harvester in publisher['harvesters']:
                harvest_dict = {
                    'name': harvester['name'],
                    'title': harvester['title'],
                    'url': harvester['url'],
                    'source_type': harvester['source_type'],
                    'owner_org': saved_publisher['id'],
                    'publisher_id': saved_publisher['id'],
                    'frequency': 'WEEKLY',
                }

                harvester_id = self._get_harvester_id(harvester['name'])
                if harvester_id is None:
                    harvest_action = 'harvest_source_create'
                    harvest_dict['id'] = str(uuid.uuid4())
                else:
                    harvest_action = 'harvest_source_update'
                    harvest_dict['id'] = harvester_id

                saved_harvesters.append(
                    toolkit.get_action(harvest_action)(self.get_context(), harvest_dict)['id']
                )

        # Delete any harvester that we haven't processed in this run
        for harvester_id in self._get_harvester_ids():
            if harvester_id not in saved_harvesters:
                toolkit.get_action('harvest_source_delete')(
                    self.get_context(), {'id': harvester_id}
                )

        # Delete any publishers that we haven't processed in this run
        for pub_id in self._get_publisher_ids():
            if pub_id not in saved_publishers:
                try:
                    toolkit.get_action('organization_delete')(self.get_context(), {'id': pub_id})
                    counts['delete'] += 1
                except ValidationError, ex:
                    print('Unable to delete publisher {}, {}'.format(pub_id, ex))

        print('Created {add}, updated {update} and deleted {delete} publishers'.format(**counts))

    def _get_publisher_id(self, publisher_name):
        try:
            pub = toolkit.get_action('organization_show')(
                self.get_context(), {'id': publisher_name}
            )
        except NotFound:
            return None
        return pub['id']

    def _get_publisher_ids(self):
        return [
            x['id'] for x in toolkit.get_action('organization_list')(
                self.get_context(), {'all_fields': True}
            )
        ]

    def _get_harvester_id(self, harvester_name):
        try:
            pub = toolkit.get_action('harvest_source_show')(
                self.get_context(), {'id': harvester_name}
            )
        except NotFound:
            return None
        return pub['id']

    def _get_harvester_ids(self):
        return [
            x['id'] for x in toolkit.get_action('harvest_source_list')(
                self.get_context(), {'all_fields': True}
            )
        ]

