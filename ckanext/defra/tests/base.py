import ckan.lib.create_test_data as ctd
from ckan.tests import helpers, factories
from ckanext.harvest.model import setup as db_setup


class BaseTestCase(helpers.FunctionalTestBase):
    _load_plugins = ['harvest', 'test_harvester']

    @classmethod
    def setup_class(cls):
        helpers.reset_db()
        super(BaseTestCase, cls).setup_class()

    @classmethod
    def teardown_class(cls):
        helpers.reset_db()

    def setup(self):
        super(BaseTestCase, self).setup()
        db_setup()
        self.app = self._get_test_app()
        ctd.CreateTestData.create()
