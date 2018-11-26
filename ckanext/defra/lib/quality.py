# Scores dataset records according to a modified version of the
# EA DQAP (Data Quality Action Plan) where those rules can be
# translated into automated checks, and aren't issues of governance
# or publishing. The entry point for this module is the score_record
# function.
#
# When/If a defra data quality action plan is approved we should
# modify these checks and also provide a cross-reference from the
# reasons we give to the action plan.
import re


def score_record(dataset):
    """
    Iterates over all of the CHECKs and invokes the function found there.
    If that function return false, that is the check failed, then the
    penalty is removed from the current total, and the reason for the failure
    is added to the list.
    """
    score = 100
    reasons = []

    for (func, penalty, reason) in CHECKS:
        if not func(dataset):
            score -= penalty
            reasons.append(reason)

    return (score or 0, reasons)


def _find_extra(dataset, key):
    for e in dataset['extras']:
        if e['key'] == key:
            return e['value']
    return None


class Checks(object):

    @classmethod
    def _skip_if_private(cls, dataset):
        vals = [e['value'] for e in dataset['extras'] if e['key'] == 'private-resources']
        return any(vals)

    @classmethod
    def resolvable_links(cls, dataset):
        if Checks._skip_if_private(dataset):
            return True

        return True

    @classmethod
    def has_resources(cls, dataset):
        if Checks._skip_if_private(dataset):
            return True

        return len(dataset['resources']) > 0

    @classmethod
    def has_frequency(cls, dataset):
        return [
            e for e in dataset['extras'] if e['key'] in
            ['frequency-of-update', 'frequency', 'update_frequency']
        ]

    @classmethod
    def valid_title(cls, dataset):
        return len(dataset.get('title', '')) > 16

    @classmethod
    def reasonable_title(cls, dataset):
        return len(dataset.get('title', '')) < 64

    @classmethod
    def unique_links(cls, dataset):
        if Checks._skip_if_private(dataset):
            return True

        resources = set([r['url'] for r in dataset['resources']])
        return len(resources) == len(dataset['resources'])

    @classmethod
    def description_long_enough(cls, dataset):
        return len(dataset['notes']) > 300

    @classmethod
    def is_acronym_free(cls, dataset):
        # We will capture this when we check the description length
        if len(dataset['notes'].strip()) == 0:
            return True

        for word in re.split('\W+', dataset['notes']):
            if word.upper() == word:  # all uppercase
                return False
        return True

    @classmethod
    def has_contacts(cls, dataset):
        vals = [
            e['value'] for e in dataset['extras'] if e['key'] in
            ['author', 'author_email', 'maintainer', 'maintainer_email']
        ]
        return any(vals)

    @classmethod
    def has_temporal_extent(cls, dataset):
        start = _find_extra(dataset, 'temporal-extent-begin')
        end = _find_extra(dataset, 'temporal-extent-end')
        return start and end

    @classmethod
    def has_licence(cls, dataset):
        return dataset.get('license_title') or dataset.get('licence_id')

    @classmethod
    def temporal_is_accurate_if_present(cls, dataset):
        from dateutil.parser import parse

        start = _find_extra(dataset, 'temporal-extent-begin')
        end = _find_extra(dataset, 'temporal-extent-end')
        if not start and not end:
            return True

        try:
            start_date = parse(start)
            end_date = parse(end)
        except Exception:
            return False

        if start_date > end_date:
            return False

        return True


CHECKS = {
    # Function, penalty, reason

    # Main metadata
    (Checks.reasonable_title, 5, "The title of this record is too long"),
    (Checks.valid_title,      5, "The title of this record is too short"),
    (Checks.description_long_enough, 10, "The description for this record is not very long/detailed"),
    (Checks.is_acronym_free,         10, "This description contains acronyms and their meaning may not be clear"),
    (Checks.has_licence,             10, "This record does not appear to specify a licence"),
    # Extras
    (Checks.has_frequency,    5, "The update frequency of this record is not set"),

    (Checks.has_temporal_extent,              5, "This record does not describe what time period (temporal extent) it covers"),
    (Checks.temporal_is_accurate_if_present,  5, "The temporal extent is inaccurate"),

    # Resources
    (Checks.has_resources,   10, "This record appears to have no data"),
    (Checks.resolvable_links, 5, "Some of the resources do not appear to work"),
    (Checks.unique_links,     5, "Resources are not unique, there are duplicates"),

    # Contacts
    (Checks.has_contacts,     5, "There is no contact information for this dataset"),
}

# Currently unimplemented from the Quality Action Plan
# 2. Data location should be right
#     2.1 Links must be valid
#         2.1.1 Should resolve
#         2.1.2 Should be http? (check... maybe not...)
#     2.4 Format should be consistent with Link
#         2.4.1 Make sure URL format matches reality

# 6. Technical contact should be right
#     6.2 Must be valid
#         6.2.1 Email address should be 'defra-group' address
#         6.2.2 Must still be employed by defra
#         6.2.3 Must be on staff list

# 8. Should all be recorded
#     8.1 Records must be unique
#         8.1.1. No duplicates (based on title)
#     8.2 Complete set of records
#         8.2.1 All datasets in data flow maps should be in catalogue
#         8.2.2 All records on NDL should appear in metadata catalogue

# 9. INSPIRE themes (where relevant) should be right
#     9.1 Should be complete (present)
#     9.2 Should be consistent

# 10 Licensing details should be right
#     10.2 Should be consistent (with use constraints) ... erm

# 11. Bounding box should be right
#     11.1 Should be complete - all four coords present
#     11.2 Should have non-zero area
#     11.3 Should be consistent with scope of title
