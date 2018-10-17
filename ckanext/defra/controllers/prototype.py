# encoding: utf-8

import ckan.plugins.toolkit as toolkit
from ckan.lib.base import c


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

        c.organisation_list = toolkit.get_action('organization_list')(
            context, {
                'all_fields': True,
                'include_dataset_count': True,
                'sort': 'package_count'
            }
        )

        return toolkit.render('reports/index.html',
                              extra_vars={})
