"""
Tests for custom Defra controllers.
"""
from base import BaseTestCase
from ckan.tests import helpers, factories
from ckanext.harvest.tests import factories as harvest_factories
import ckan.lib.create_test_data as ctd


class TestSearchController(BaseTestCase):
    def test_dataset_autocomplete(self):
        ds1 = factories.Dataset(name='test-dataset-1', title='First test dataset')
        factories.Dataset(name='test-dataset-2', title='Second test dataset')
        response = self.app.get(u'/search/autocomplete?q=first')
        assert len(response.json['Datasets']) == 1, 'Expected 1 dataset'
        assert response.json['Datasets'][0]['name'] == ds1['name'], 'Invalid search result returned'
        response = self.app.get(u'/search/autocomplete?q=test-dataset')
        assert len(response.json['Datasets']) == 2, 'Expected 2 datasets'

    def test_organization_autocomplete(self):
        org1 = factories.Organization(name='test-org-1', title='First test organization')
        factories.Organization(name='test-org-2', title='Second test organization')
        response = self.app.get(u'/search/autocomplete?q=first')
        assert len(response.json['Publishers']) == 1, 'Expected 1 organization'
        assert response.json['Publishers'][0]['name'] == org1['name'], 'Invalid search result returned'
        response = self.app.get(u'/search/autocomplete?q=test-org')
        assert len(response.json['Publishers']) == 2, 'Expected 2 organizations'

    def test_harvester_autocomplete(self):
        source1 = harvest_factories.HarvestSource(title='First test harvester')
        harvest_factories.HarvestSource(title='Second test harvester')
        response = self.app.get(u'/search/autocomplete?q=first')
        assert len(response.json['Harvesters']) == 1, 'Expected 1 harvester'
        assert response.json['Harvesters'][0]['title'] == source1['title'], \
            'Invalid search result returned'
        response = self.app.get(u'/search/autocomplete?q=test')
        assert len(response.json['Harvesters']) == 2, 'Expected 2 harvesters'

    def test_publisher_filter(self):
        org1 = factories.Organization(id='test-org', name='test-org', title='Test organization')
        factories.Dataset(owner_org=org1['id'])
        response = self.app.get(u'/search/autocomplete?q=&publisher=test-org')
        assert len(response.json['Datasets']) == 1, 'Expected 1 dataset'
        assert len(response.json['Publishers']) == 0, 'Expected 0 organizations'
        assert len(response.json['Harvesters']) == 0, 'Expected 0 harvesters'
