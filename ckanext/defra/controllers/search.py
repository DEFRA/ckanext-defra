# encoding: utf-8
import json

import ckan.plugins.toolkit as toolkit
from ckan.common import response


class SearchController(toolkit.BaseController):
    def autocomplete(self):
        query = toolkit.request.params.get('q')
        autocomplete_response = {
            'packages': toolkit.get_action('package_autocomplete')({}, {'q': query, 'limit': 5}),
            'organizations': toolkit.get_action('organization_autocomplete')({}, {'q': query, 'limit': 5}),
        }
        response.status_int = 200
        response.content_type = 'application/json; charset=utf-8'
        return json.dumps(autocomplete_response)
