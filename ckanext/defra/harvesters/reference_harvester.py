from ckan.plugins.core import SingletonPlugin, implements
from ckanext.harvest.interfaces import IHarvester

from urlparse import urlparse
import requests


class ReferenceDataHarvester(SingletonPlugin):
    '''
    A harvester for the Defra Reference Data Service
    '''
    implements(IHarvester)

    def info(self):
        '''
        :returns: A dictionary with the harvester descriptors
        '''
        return {
            'name': 'rds',
            'title': 'Defra Reference Data Service',
            'description': 'An instance of the Defra Reference Data Service'
        }

    def gather_stage(self, harvest_job):
        '''
        Make a request to the API endpoint for metadata and create a
        harvestobject for each namespace/entity dataset.

        The gather stage will receive a HarvestJob object and will be
        responsible for:
            - gathering all the necessary objects to fetch on a later.
            stage (e.g. for a CSW server, perform a GetRecords request)
            - creating the necessary HarvestObjects in the database, specifying
            the guid and a reference to its job. The HarvestObjects need a
            reference date with the last modified date for the resource, this
            may need to be set in a different stage depending on the type of
            source.
            - creating and storing any suitable HarvestGatherErrors that may
            occur.
            - returning a list with all the ids of the created HarvestObjects.
            - to abort the harvest, create a HarvestGatherError and raise an
            exception. Any created HarvestObjects will be deleted.

        :param harvest_job: HarvestJob object
        :returns: A list of HarvestObject ids
        '''
        url = urlparse(harvest_job.source.url)
        if url.path != "/api/1":
            url = "{}://{}/api/1".format(url.scheme, url.netloc)

        try:
            content = requests.get(url).json()
            print content
        except Exception as e:
            print e

    def fetch_stage(self, harvest_object):
        '''
        The fetch stage will receive a HarvestObject object and will be
        responsible for:
            - getting the contents of the remote object (e.g. for a CSW server,
            perform a GetRecordById request).
            - saving the content in the provided HarvestObject.
            - creating and storing any suitable HarvestObjectErrors that may
            occur.
            - returning True if everything is ok (ie the object should now be
            imported), "unchanged" if the object didn't need harvesting after
            all (ie no error, but don't continue to import stage) or False if
            there were errors.

        :param harvest_object: HarvestObject object
        :returns: True if successful, 'unchanged' if nothing to import after
                all, False if not successful
        '''

    def import_stage(self, harvest_object):
        '''
        The import stage will receive a HarvestObject object and will be
        responsible for:
            - performing any necessary action with the fetched object (e.g.
            create, update or delete a CKAN package).
            Note: if this stage creates or updates a package, a reference
            to the package should be added to the HarvestObject.
            - setting the HarvestObject.package (if there is one)
            - setting the HarvestObject.current for this harvest:
            - True if successfully created/updated
            - False if successfully deleted
            - setting HarvestObject.current to False for previous harvest
            objects of this harvest source if the action was successful.
            - creating and storing any suitable HarvestObjectErrors that may
            occur.
            - creating the HarvestObject - Package relation (if necessary)
            - returning True if the action was done, "unchanged" if the object
            didn't need harvesting after all or False if there were errors.

        NB You can run this stage repeatedly using 'paster harvest import'.

        :param harvest_object: HarvestObject object
        :returns: True if the action was done, "unchanged" if the object didn't
                need harvesting after all or False if there were errors.
        '''
