# A prototype report for showing the quality of the metadata that we have
# retrieved.  Currently this just gives every dataset a score of 100 and
# then removes points for bad metadata.  At present we only have a couple
# of criteria, but we can always add others in the rank_dataset function.

import ckan.plugins.toolkit as toolkit


def bad_record(dataset, reasons):
    return {
        'name': dataset['name'],
        'title': dataset['title'],
        'reasons': reasons
    }


def rank_dataset(dataset):
    score = 100
    reasons = []

    if len(dataset['notes']) < 100:
        score -= 10
        reasons.append("The description is very short")

    if len(dataset['resources']) == 0:
        score -= 10
        reasons.append("There are no data resources for this record")

    freq_key = [
        e for e in dataset['extras'] if e['key'] in ['frequency-of-update', 'frequency', 'update_frequency']
    ]
    if not freq_key:
        score -= 5
        reasons.append("The update frequency is not specified")

    return (score or 0, reasons)


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
            (score, reasons) = rank_dataset(dataset)
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
