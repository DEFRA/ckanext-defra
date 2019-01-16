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

    def collections_home(self):
        return toolkit.render('collection/index.html',
                              extra_vars={})

    def collections_page(self, id):

        c.package1 = toolkit.get_action('package_show')({}, {'id': 'historic-flood-event-outlines'})
        c.package2 = toolkit.get_action('package_show')({}, {'id': 'flood-defences'})
        c.package3 = toolkit.get_action('package_show')({}, {'id': 'remotelysensedfloodestimates'})


        return toolkit.render('collection/{}.html'.format(id),
                              extra_vars={})
