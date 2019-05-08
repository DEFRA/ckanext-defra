"""
Tests for custom Defra controllers.
"""
from base import BaseTestCase
from ckan.tests import helpers, factories


class TestSearchController(BaseTestCase):
    def test_dataset_autocomplete(self):
        ds1 = factories.Dataset(name='test-dataset-1', title='First test dataset')
        factories.Dataset(name='test-dataset-2', title='Second test dataset')

        response = self.app.get(u'/search/autocomplete?q=first')
        assert len(response.json['packages']) == 1, 'Expected 1 dataset'
        assert response.json['packages'][0]['name'] == ds1['name'], 'Invalid search result returned'

        response = self.app.get(u'/search/autocomplete?q=test-dataset')
        assert len(response.json['packages']) == 2, 'Expected 2 datasets'

    def test_organization_autocomplete(self):
        org1 = factories.Dataset(name='test-org-1', title='First test organization')
        factories.Dataset(name='test-org-2', title='Second test organization')
        response = self.app.get(u'/search/autocomplete?q=first')
        assert len(response.json['organizations']) == 1, 'Expected 1 organization'
        assert response.json['packages'][0]['name'] == org1['name'], 'Invalid search result returned'

        response = self.app.get(u'/search/autocomplete?q=test-dataset')
        assert len(response.json['organizations']) == 2, 'Expected 2 organizations'
