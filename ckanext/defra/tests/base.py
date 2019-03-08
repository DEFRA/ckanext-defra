import ckan.lib.create_test_data as ctd
from ckan.tests.helpers import FunctionalTestBase
from ckanext.harvest.model import setup as db_setup


class BaseTestCase(FunctionalTestBase):
    _load_plugins = ['harvest']

    @classmethod
    def setup_class(cls):
        super(BaseTestCase, cls).setup_class()
        ctd.CreateTestData.create()

    def setup(self):
        super(BaseTestCase, self).setup()
        db_setup()
