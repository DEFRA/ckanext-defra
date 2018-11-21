# A prototype report for showing the quality of the metadata that we have
# retrieved.  Currently this just gives every dataset a score of 100 and
# then removes points for bad metadata.  At present we only have a couple
# of criteria, but we can always add others in the rank_dataset function.

import ckan.plugins.toolkit as toolkit
from ckanext.defra.lib.quality import score_record

def bad_record(dataset, reasons):
    return {
        'name': dataset['name'],
        'title': dataset['title'],
        'reasons': reasons
    }


def quality_report():
    # PROTOTYPE quality report which measures the quality of metadata within
    # a publisher
    table = []
    context = {}

    organisation_list = toolkit.get_action('organization_list')(
        context, {
            'all_fields': True,
            'include_datasets': True
        }
    )

    for organisation in organisation_list:
        bad_entries = []
        entry = {
         'name': organisation['name'],
         'title': organisation['title'],
         'average': 0,
         'record_count': 0,
         'worst_offenders': []
        }

        datasets = toolkit.get_action('package_search')(
            context, {
                'q': 'owner_org:{}'.format(organisation['id']),
                'rows': 10000
            }
        )['results']

        ranked = []
        for dataset in datasets:
            (score, reasons) = score_record(dataset)
            entry['record_count'] += 1
            entry['average'] += score

            ranked.append((score, bad_record(dataset, reasons)))

        if entry['record_count'] > 0:
            entry['average'] /= entry['record_count']

        ranked.sort(key=lambda t: t[0])
        bad_entries = [r for r in ranked if r[0] < 100][0:5]

        entry['worst_offenders'] = bad_entries
        table.append(entry)

    return {
        'table': table
    }
