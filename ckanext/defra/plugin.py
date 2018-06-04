import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.lib.plugins import DefaultTranslation
from ckan.config.routing import SubMapper

import ckanext.defra.schema as schema_defs


class DefraPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm, DefaultTranslation):
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_public_directory(config, 'public')

    # IRoutes
    def before_map(self, routes):
        routes.redirect('/organization/{url:.*}', '/publisher/{url}')        
        return routes

    def after_map(self, routes):
        # delete_routes_by_path_startswith(routes, '/organization')

        with SubMapper(routes, controller='ckanext.defra.controllers.publisher:PublisherController') as m:
            m.connect('publishers_index', '/publisher', action='index')
            m.connect('publisher_index', '/publisher', action='index')
            m.connect('publisher_new', '/publisher/new', action='new')
            for action in [
            'delete',
            'admins',
            'member_new',
            'member_delete',
            'history']:
                m.connect('publisher_' + action,
                        '/publisher/' + action + '/{id}',
                        action=action)

            m.connect('publisher_activity', '/publisher/activity/{id}/{offset}',
                    action='activity')
            m.connect('publisher_read', '/publisher/{id}', action='read')
            m.connect('publisher_about', '/publisher/about/{id}',
                    action='about')
            m.connect('publisher_read', '/publisher/{id}', action='read',
                    ckan_icon='sitemap')
            m.connect('publisher_edit', '/publisher/edit/{id}',
                    action='edit')
            m.connect('publisher_members', '/publisher/members/{id}',
                    action='members')
            m.connect('publisher_bulk_process',
                    '/publisher/bulk_process/{id}',
                    action='bulk_process')

        return routes

    # ITemplateHelpers
    def get_helpers(self):
        from inspect import getmembers, isfunction
        import ckanext.defra.helpers as h

        helper_dict = {}

        functions_list = [o for o in getmembers(h, isfunction)]
        for name, fn in functions_list:
            if name[0] != '_':
                helper_dict[name] = fn
        return helper_dict



def delete_routes_by_path_startswith(map, path_startswith):
    """
    This function will remove from the routing map any
    path that starts with the provided argument (/ required).

    Not really a great thing to be doing, but CKAN doesn't
    provide a way to i18n URLs because it'll likely cause
    clashes with other group subclasses.
    """
    matches_to_delete = []
    for match in map.matchlist:
        if match.routepath.startswith(path_startswith):
            matches_to_delete.append(match)
    for match in matches_to_delete:
        map.matchlist.remove(match)
