# encoding: utf-8

import re

import ckan.controllers.organization as org
import ckan.plugins as plugins


class PublisherController(org.OrganizationController):
    ''' The organization controller is for Organizations, which are implemented
    as Groups with is_organization=True and group_type='organization'. It works
    the same as the group controller apart from:
    * templates and logic action/auth functions are sometimes customized
      (switched using _replace_group_org)
    * 'bulk_process' action only works for organizations
    Nearly all the code for both is in the GroupController (for historical
    reasons).
    '''

    group_types = ['organization', 'publisher']

    def _replace_group_org(self, string):
        ''' substitute organization for group if this is an org'''
        return re.sub('^group', 'organization', string)

    def _update_facet_titles(self, facets, group_type):
        for plugin in plugins.PluginImplementations(plugins.IFacets):
            facets = plugin.organization_facets(facets, group_type, None)

    def _guess_group_type(self, expecting_name=False):
        return 'organization'
