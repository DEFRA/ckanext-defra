# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from ckan.lib.base import c
from ckan import model


class PrototypeController(toolkit.BaseController):

    def more(self, id):
        context = {}
        c.pkg_dict = toolkit.get_action('package_show')(
            context, {'id': id}
        )
        c.pkg = context['package']

        return toolkit.render('package/more.html',
                              extra_vars={'pkg_dict': c.pkg_dict})

    def reports(self):
        context = {}

        # Retrieve a list of the 5 most recently modified packages
        c.modified_packages = toolkit.get_action('package_search')(
            context, {
                'q': '',
                'sort': 'metadata_modified desc',
                'rows': 5
            }
        )['results']

        # Retrieve the 5 most recently added packages, but don't
        # yet make them available
        res = toolkit.get_action('package_search')(
            context, {
                'q': '',
                'sort': 'metadata_created desc',
                'rows': 5
            }
        )

        # Pluck the total number of datasets before we assign the
        # results from the previous call
        pkg_total = res['count']
        c.new_packages = res['results']

        # org count
        org_count = len(toolkit.get_action('organization_list')(context, {}))

        # Number of harvesters
        harvester_count = len(toolkit.get_action('harvest_source_list')(
            context, {}
        ))

        # Number of resources...
        resource_count = model.Session.query(model.Resource).filter(model.Resource.state == 'active')


        c.statistics = {
            'harvester_count': harvester_count,
            'dataset_count': pkg_total,
            'organisation_count': org_count,
            'resource_count': resource_count.count()
        }

        return toolkit.render('reports/index.html',
                              extra_vars={})

    def reports_publishing(self):
        context = {}

        c.organisation_list = toolkit.get_action('organization_list')(
            context, {
                'all_fields': True,
                'include_dataset_count': True,
                'sort': 'package_count'
            }
        )

        return toolkit.render('reports/publishing.html',
                              extra_vars={})

    def reports_access(self):
        context = {}

        c.organisation_list = toolkit.get_action('organization_list')(
            context, {
                'all_fields': True,
                'include_dataset_count': True,
                'sort': 'package_count'
            }
        )

        return toolkit.render('reports/access.html',
                              extra_vars={})

    def reports_broken(self):
        context = {}

        c.organisation_list = toolkit.get_action('organization_list')(
            context, {
                'all_fields': True,
                'include_dataset_count': True,
                'sort': 'package_count'
            }
        )

        return toolkit.render('reports/broken.html',
                              extra_vars={})
