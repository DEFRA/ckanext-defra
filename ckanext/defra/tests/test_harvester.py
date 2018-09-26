from ckan.tests.helpers import FunctionalTestBase
from ckanext.harvest.tests.factories import (HarvestSourceObj, HarvestJobObj)
from ckanext.defra.harvesters.reference_harvester import ReferenceDataHarvester


class TestReferenceHarvester(FunctionalTestBase):

    def test_gather(self):
        source = HarvestSourceObj(url='http://localhost/')
        job = HarvestJobObj(source=source)

        harvester = ReferenceDataHarvester()
        object_ids = harvester.gather_stage(job)
        assert object_ids == []

    def test_fetch(self):
        pass

    def test_import(self):
        pass