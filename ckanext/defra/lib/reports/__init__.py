from ckanext.defra.lib.reports.publishing_reports import publishing_history_report
from ckanext.defra.lib.reports.access_reports import access_history_report
from ckanext.defra.lib.reports.broken_resource_reports import broken_resource_report


publishing_report = {
    'name': 'publishing',
    'description': 'The publishing history of datasets for each organisation',
    'option_defaults': {},
    'option_combinations': None,
    'generate': publishing_history_report,
    'template': 'report/publishing.html'
}

access_history_report = {
    'name': 'access',
    'description': 'The access history of datasets, by department',
    'option_defaults': {},
    'option_combinations': None,
    'generate': access_history_report,
    'template': 'report/access.html'
}

broken_resource_report = {
    'name': 'broken',
    'description': 'The percentage of broken records',
    'option_defaults': {},
    'option_combinations': None,
    'generate': broken_resource_report,
    'template': 'report/broken.html'
}