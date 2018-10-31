from ckanext.defra.lib.reports.publishing_reports import publishing_history_report
from ckanext.defra.lib.reports.access_reports import access_history_report
from ckanext.defra.lib.reports.broken_resource_reports import broken_resource_report


publishing_report = {
    'name': 'publishing',
    'description': ('For each organisation, this report shows both the addition on new dataset records and '
                    'the modification of those records for the current year, 2018.'
    ),
    'option_defaults': {},
    'option_combinations': None,
    'generate': publishing_history_report,
    'template': 'report/publishing.html'
}

access_history_report = {
    'name': 'access',
    'description': ('This report shows both how often a dataset record was viewed in a browser, '
                    'and how often a dataset from that organisation appeared in search results'
    ),
    'option_defaults': {},
    'option_combinations': None,
    'generate': access_history_report,
    'template': 'report/access.html'
}

broken_resource_report = {
    'name': 'broken',
    'description': ('The percentage of broken records, per organisation. A broken record is a link to '
                    'a data resource which no longer works. This often happens when sites are redesigned'
                    ' but the metadata record is not updated.'
    ),
    'option_defaults': {},
    'option_combinations': None,
    'generate': broken_resource_report,
    'template': 'report/broken.html'
}