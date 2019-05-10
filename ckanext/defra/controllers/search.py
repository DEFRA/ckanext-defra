# encoding: utf-8
import json

import ckan.plugins.toolkit as toolkit
from ckan.common import response
from ckan import model
from ckan.lib.base import c

class SearchController(toolkit.BaseController):
    def autocomplete(self):
        query = toolkit.request.params.get('q', '')
        publisher = toolkit.request.params.get('publisher', None)
        package_q = 'name:{query}* OR title:{query}*'.format(query=query)
        package_fq = 'organization:{}'.format(publisher) \
            if publisher is not None else ''

        harvesters = []
        harvest_packages = toolkit.get_action('package_search')({}, {
            'q': package_q,
            'fq': package_fq + ' +dataset_type:harvest',
            'rows': 5
        })
        for harvester in harvest_packages['results']:
            if query.lower() in harvester['title'].lower():
                harvesters.append({
                    'id': harvester['id'],
                    'name': harvester['title'],
                    'title': harvester['title'],
                })

        packages = toolkit.get_action('package_search')({}, {
            'q': package_q,
            'fq': package_fq,
            'rows': 5
        })
        datasets = []
        for dataset in packages['results']:
            datasets.append({
                'name': dataset['name'],
                'title': dataset['title'],
            })

        publishers = []
        if publisher is None:
            publishers = toolkit.get_action('organization_autocomplete')({}, {
                'q': query, 'limit': 5
            })
            for publisher in publishers:
                publisher['title'] += ' ({})'.format(publisher['name'].upper())

        response.status_int = 200
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps({
            'Publishers': publishers,
            'Datasets': datasets,
            'Harvesters': harvesters,
        })
