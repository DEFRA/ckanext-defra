from ckan.common import _

def dashboard_show(context, data_dict):
    if context.get('user'):
        return {'success': True}
    else:
        return {'success': False,
                'msg': _("Only logged in users can see dashboards")}