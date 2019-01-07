import ckan.plugins.toolkit as toolkit


def _get_records(offset=0):
    return toolkit.get_action('package_search')({}, {
        'q': '',
        'rows': 1000,
        'start': offset
    })


def get_all_datasets():
    response = _get_records(0)
    total_records = response['count']
    datasets = response['results']
    while len(datasets) != total_records:
        response = _get_records(len(datasets))
        datasets += response['results']
    return datasets
