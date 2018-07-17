# encoding: utf-8
import ckan.lib.base as base
import ckan.plugins.toolkit as toolkit
from ckan import model


class LocationController(base.BaseController):

    def index(self):
        context = {'model': model, 'session': model.Session,
                   'user': toolkit.c.user, 'for_view': True,
                   'with_private': False}

        try:
            toolkit.check_access('site_read', context)
        except toolkit.NotAuthorized:
            toolkit.abort(403, toolkit._('Not authorized to see this page'))

        if toolkit.c.userobj:
            context['user_id'] = toolkit.c.userobj.id
            context['user_is_admin'] = toolkit.c.userobj.sysadmin

        try:
            pass
        except toolkit.ValidationError:
            return toolkit.render('location/index.html')

        return toolkit.render('location/index.html')
