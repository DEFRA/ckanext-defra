# encoding: utf-8
import ckan.plugins.toolkit as toolkit
import ckan.lib.base as base
import ckan.model as model
import ckan.logic as logic
from ckan.lib.base import c
from ckan.common import _


class DatasetController(toolkit.BaseController):
    def __before__(self, action, **kwargs):
        super(DatasetController, self).__before__(action, **kwargs)
        context = {
            'model': model,
            'user': c.user,
            'auth_user_obj': c.userobj
        }
        try:
            logic.check_access('sysadmin', context, {})
        except logic.NotAuthorized:
            if c.action not in ('more',):
                base.abort(403, _('Not authorized to see this page'))

    def more(self, dataset_id):
        context = {}
        c.pkg_dict = toolkit.get_action('package_show')(
            context, {'id': dataset_id}
        )
        c.pkg = context['package']

        return toolkit.render('package/more.html', extra_vars={'pkg_dict': c.pkg_dict})

    def issues(self, dataset_id):
        context = {}
        c.pkg_dict = toolkit.get_action('package_show')(
            context, {'id': dataset_id}
        )
        c.pkg = context['package']
        return toolkit.render('package/issues.html', extra_vars={'pkg_dict': c.pkg_dict})
