import collections
import sys
import uuid
from urlparse import urljoin

import ckan.plugins.toolkit as toolkit


PublisherStub = collections.namedtuple('PublisherStub', ['name', 'title', 'image_url', 'dgu_name'])


class ImportPublishersCommand(toolkit.CkanCommand):
    ''' Imports all of the publishers for Defra (inc. defra) '''
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0

    def command(self):
        self.context = {
            'ignore_auth': True,
        }

        self._load_config()

        self.site_url = toolkit.config.get("ckan.site_url")

        for publisher in PUBLISHERS:
            action = 'organization_update'
            publisher_dict = self.existing_publisher(publisher)
            if not publisher_dict:
                action = 'organization_create'
                publisher_dict = self.publisher_to_dict(publisher)

            publisher_dict['name'] = publisher.name
            publisher_dict['title'] = publisher.title
            if publisher.image_url:
                publisher_dict['image_url'] = urljoin(self.site_url, publisher.image_url)

            toolkit.get_action(action)(
                self.context, publisher_dict
            )


    def existing_publisher(self, publisher):
        try:
            pub = toolkit.get_action('group_show')(
                self.context, {'id': publisher.name}
            )
            return pub
        except:
            pass

        return None

    def publisher_to_dict(self, publisher):
        return {
            'id': str(uuid.uuid4()),
        }

PUBLISHERS = [
    PublisherStub(
        name='defra',
        dgu_name='department-for-environment-food-and-rural-affairs',
        title='Department for Environment, Food & Rural Affairs',
        image_url='/images/defra.png'
    ),
    PublisherStub(
        name='gc',
        dgu_name='forestry-commission',
        title='Forestry Commission',
        image_url='/images/forestry-commission.png'
    ),
    PublisherStub(
        name='wsra',
        dgu_name='water-services-regulation-authority',
        title='The Water Services Regulation Authority',
        image_url='/images/the-water-services-regulation-authority.png'
    ),
    PublisherStub(
        name='apha',
        dgu_name='animal-and-plant-health-agency',
        title='Animal and Plant Health Agency',
        image_url='/images/apha.png'
    ),
    PublisherStub(
        name='cefas',
        dgu_name='centre-for-environment-fisheries-aquaculture-science',
        title='Centre for Environment, Fisheries and Aquaculture Science',
        image_url='/images/cefas.png'
    ),
    PublisherStub(
        name='rpa',
        dgu_name='rural-payments-agency',
        title='Rural Payments Agency',
        image_url='/images/rpa.png'
    ),
    PublisherStub(
        name='vmd',
        dgu_name='veterinary-medicines-directorate',
        title='Veterinary Medicines Directorate',
        image_url='/images/vmd.png'
    ),
    PublisherStub(
        name='ahdb',
        dgu_name='',
        title='Agriculture and Horticulture Development Board',
        image_url=''
    ),
    PublisherStub(
        name='kew',
        dgu_name='royal-botanic-gardens-kew',
        title='Board of Trustees of the Royal Botanic Gardens Kew',
        image_url=''
    ),
    PublisherStub(
        name='ccw',
        dgu_name='consumer-council-for-water',
        title='Consumer Council for Water',
        image_url=''
    ),
    PublisherStub(
        name='ea',
        dgu_name='environment-agency',
        title='Environment Agency',
        image_url=''
    ),
    PublisherStub(
        name='jncc',
        dgu_name='joint-nature-conservation-committee',
        title='Joint Nature Conservation Committee',
        image_url=''
    ),
    PublisherStub(
        name='mmo',
        dgu_name='marine-management-organisation',
        title='Marine Management Organisation',
        image_url=''
    ),
    PublisherStub(
        name='nfc',
        dgu_name='national-forest-company',
        title='National Forest Company',
        image_url=''
    ),
    PublisherStub(
        name='ne',
        dgu_name='natural-england',
        title='Natural England',
        image_url=''
    ),
    PublisherStub(
        name='sfia',
        dgu_name='sea-fish-industry-authority',
        title='Sea Fish Industry Authority',
        image_url=''
    ),
    PublisherStub(
        name='acre',
        dgu_name='',
        title='Advisory Committee on Releases to the Environment',
        image_url=''
    ),
    PublisherStub(
        name='iaap',
        dgu_name='',
        title='Independent Agricultural Appeals Panel',
        image_url=''
    ),
    PublisherStub(
        name='sac',
        dgu_name='',
        title='Science Advisory Council',
        image_url=''
    ),
    PublisherStub(
        name='vpc',
        dgu_name='',
        title='Veterinary Products Committee',
        image_url=''
    ),
    PublisherStub(
        name='pvst',
        dgu_name='',
        title='Plant Varieties and Seeds Tribunal',
        image_url=''
    ),
    PublisherStub(
        name='dnpa',
        dgu_name='dartmoor-national-park-authority',
        title='Dartmoor National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='dwi',
        dgu_name='',
        title='Drinking Water Inspectorate',
        image_url=''
    ),
    PublisherStub(
        name='enpa',
        dgu_name='exmoor-national-park',
        title='Exmoor National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='ldnpa',
        dgu_name='lake-district-national-park',
        title='Lake District National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='nfnpa',
        dgu_name='new-forest-national-park',
        title='New Forest National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='nymnpa',
        dgu_name='north-york-moors-national-park-authority',
        title='North York Moors National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='nnpa',
        dgu_name='northumberland-national-park-authority',
        title='Northumberland National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='pdnpa',
        dgu_name='peak-district-national-park-authority',
        title='Peak District National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='sdnpa',
        dgu_name='south-downs-national-park-authority',
        title='South Downs National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='ukcb',
        dgu_name='',
        title='UK Co-ordinating Body',
        image_url=''
    ),
    PublisherStub(
        name='ydnpa',
        dgu_name='yorkshire-dales-national-park-authority',
        title='Yorkshire Dales National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='ba',
        dgu_name='broads-authority',
        title='Broads Authority',
        image_url=''
    ),
    PublisherStub(
        name='cgma',
        dgu_name='',
        title='Covent Garden Market Authority',
        image_url=''
    ),
]
