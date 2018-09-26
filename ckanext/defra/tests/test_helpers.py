from ckan.tests.helpers import FunctionalTestBase

import ckanext.defra.helpers as h


def fake_package():
    return {
        'extras': [
            {'key': 'key', 'value': 'value'},
            {'key': 'KEY', 'value': 'VALUE'},
            {'key': 'release-notes', 'value': 'release notes'}
        ]
    }


class TestHelpers(FunctionalTestBase):
    def test_finding_release_notes(self):
        pkg = fake_package()
        assert(h.release_notes(pkg) == 'release notes')

    def test_finding_extras(self):
        pkg = fake_package()
        assert(h._find_extra(pkg, 'nope') is None)
        assert(h._find_extra(pkg, '') is None)
        assert(h._find_extra(pkg, None) is None)
        assert(h._find_extra(pkg, 'key') == 'value')
