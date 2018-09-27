# encoding: utf-8

import re

import ckan.plugins.toolkit as toolkit
import ckan.plugins as plugins
from ckan import model

from ckan.lib.base import h, c



class PrototypeController(toolkit.BaseController):

    def more(self, id):
        context = {}
        c.pkg_dict = toolkit.get_action('package_show')(
            context, {'id': id}
        )
        c.pkg = context['package']

        return toolkit.render('package/more.html',
                          extra_vars={'pkg_dict': c.pkg_dict })