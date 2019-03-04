# encoding: utf-8

import re

import ckan.controllers.organization as org

import ckan.plugins.toolkit as toolkit
import ckan.plugins as plugins
from ckan import model

from ckan.lib.base import h


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

    def read(self, id):
        return super(org.OrganizationController, self).read(id)

    def index(self):
        group_type = self._guess_group_type()

        page = h.get_page_number(toolkit.request.params) or 1
        items_per_page = 50

        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user, 'for_view': True,
                   'with_private': False}

        q = toolkit.c.q = toolkit.request.params.get('q', '')
        sort_by = toolkit.c.sort_by_selected = toolkit.request.params.get('sort')
        startswith = toolkit.request.params.get('startswith')

        try:
            self._check_access('site_read', context)
            self._check_access('group_list', context)
        except toolkit.NotAuthorized:
            toolkit.abort(403, _('Not authorized to see this page'))

        # pass user info to context as needed to view private datasets of
        # orgs correctly
        if toolkit.c.userobj:
            context['user_id'] = toolkit.c.userobj.id
            context['user_is_admin'] = toolkit.c.userobj.sysadmin

        try:
            data_dict_global_results = {
                'all_fields': True,
                'q': q,
                'sort': sort_by,
                'type': group_type or 'group',
                'include_extras': True,
            }
            global_results = self._action('group_list')(
                context, data_dict_global_results)
        except toolkit.ValidationError as e:
            if e.error_dict and e.error_dict.get('message'):
                msg = e.error_dict['message']
            else:
                msg = str(e)
            h.flash_error(msg)
            toolkit.c.page = h.Page([], 0)
            return toolkit.render(
                self._index_template(group_type),
                extra_vars={'group_type': group_type}
            )

        start = items_per_page * (page - 1)
        end = start + items_per_page
        page_results = global_results
        if startswith is not None:
            page_results = [x for x in global_results if x['name'][0].lower() == startswith]

        toolkit.c.page = h.Page(
            collection=page_results,
            page=page,
            url=h.pager_url,
            items_per_page=items_per_page,
        )

        toolkit.c.page.items = page_results[start:end]
        return toolkit.render(
            self._index_template(group_type),
            extra_vars={
                'total_orgs': len(global_results),
                'group_type': group_type,
                'org_initials': set([x['name'][0].lower() for x in global_results]),
            }
        )
