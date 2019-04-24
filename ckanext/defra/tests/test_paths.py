import ckan.plugins.toolkit as toolkit
from base import BaseTestCase


class TestHelpers(BaseTestCase):
    def test_read_path(self):
        path = toolkit.url_for('organization_read', id='roger')
        assert(path == '/organization/roger')

    def test_edit_path(self):
        path = toolkit.url_for('organization_edit', id='roger')
        assert(path == '/organization/edit/roger')
