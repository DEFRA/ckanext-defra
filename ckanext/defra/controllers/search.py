# encoding: utf-8
import json
import re

import ckan.plugins.toolkit as toolkit
from ckan.common import response

from ckanext.defra.helpers import is_lucene


class SearchController(toolkit.BaseController):
    def _json_response(self, data):
        response.status_int = 200
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps(data)

    def autocomplete(self):
        query = toolkit.request.params.get('q', '')
        resp = {
            'Publishers': [],
            'Datasets': [],
            'Harvesters': [],
        }

        if is_lucene(query):
            return self._json_response(resp)

        publisher = toolkit.request.params.get('publisher', None)
        package_q = 'name:{query}* OR title:{query}*'.format(query=query)
        package_fq = 'organization:{}'.format(publisher) \
            if publisher is not None else ''

        harvest_packages = toolkit.get_action('package_search')({}, {
            'q': package_q,
            'fq': package_fq + ' +dataset_type:harvest',
            'rows': 5
        })
        for harvester in harvest_packages['results']:
            if query.lower() in harvester['title'].lower():
                resp['Harvesters'].append({
                    'id': harvester['id'],
                    'name': harvester['title'],
                    'title': harvester['title'],
                })

        packages = toolkit.get_action('package_search')({}, {
            'q': package_q,
            'fq': package_fq + ' +dataset_type:dataset',
            'rows': 5
        })
        for dataset in packages['results']:
            resp['Datasets'].append({
                'name': dataset['name'],
                'title': dataset['title'],
            })

        if publisher is None:
            publishers = toolkit.get_action('organization_autocomplete')({}, {
                'q': query, 'limit': 5
            })
            for publisher in publishers:
                publisher['title'] += ' ({})'.format(publisher['name'].upper())
                resp['Publishers'].append(publisher)

        return self._json_response(resp)
