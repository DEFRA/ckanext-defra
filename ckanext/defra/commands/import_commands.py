import collections 
import sys
import uuid 
from urlparse import urljoin

import ckan.plugins.toolkit as toolkit 

PublisherStub = collections.namedtuple('PublisherStub', ['name', 'title', 'image_url'])

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

            result = toolkit.get_action(action)(
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
        title='Department for Environment, Food & Rural Affairs',
        image_url='/images/defra.png'
    ),
    PublisherStub(
        name='forestry-commission', 
        title='Forestry Commission',
        image_url='/images/forestry-commission.png'
    ),    
    PublisherStub(
        name='the-water-services-regulation-authority', 
        title='The Water Services Regulation Authority',
        image_url='/images/the-water-services-regulation-authority.png'
    ),        
    PublisherStub(
        name='apha', 
        title='Animal and Plant Health Agency',
        image_url='/images/apha.png'
    ),        
    PublisherStub(
        name='cefas', 
        title='Centre for Environment, Fisheries and Aquaculture Science',
        image_url='/images/cefas.png'
    ),        
    PublisherStub(
        name='rpa', 
        title='Rural Payments Agency',
        image_url='/images/rpa.png'
    ),        
    PublisherStub(
        name='vmd', 
        title='Veterinary Medicines Directorate',
        image_url='/images/vmd.png'
    ),        
    PublisherStub(
        name='ahdb', 
        title='Agriculture and Horticulture Development Board',
        image_url=''
    ),                            
    PublisherStub(
        name='kew', 
        title='Board of Trustees of the Royal Botanic Gardens Kew',
        image_url=''
    ),                            
    PublisherStub(
        name='ccw', 
        title='Consumer Council for Water',
        image_url=''
    ),                            
    PublisherStub(
        name='ea', 
        title='Environment Agency',
        image_url=''
    ),                            
    PublisherStub(
        name='jncc', 
        title='Joint Nature Conservation Committee',
        image_url=''
    ),                            
    PublisherStub(
        name='mmo', 
        title='Marine Management Organisation',
        image_url=''
    ),                            
    PublisherStub(
        name='nfc', 
        title='National Forest Company',
        image_url=''
    ),                                                    
    PublisherStub(
        name='ne', 
        title='Natural England',
        image_url=''
    ),
    PublisherStub(
        name='sfia', 
        title='Sea Fish Industry Authority',
        image_url=''
    ),
    PublisherStub(
        name='acre', 
        title='Advisory Committee on Releases to the Environment',
        image_url=''
    ),
    PublisherStub(
        name='iaap', 
        title='Independent Agricultural Appeals Panel',
        image_url=''
    ),
    PublisherStub(
        name='sac', 
        title='Science Advisory Council',
        image_url=''
    ),                  
    PublisherStub(
        name='vpc', 
        title='Veterinary Products Committee',
        image_url=''
    ),                  
    PublisherStub(
        name='pvst', 
        title='Plant Varieties and Seeds Tribunal',
        image_url=''
    ),                  
    PublisherStub(
        name='dnpa', 
        title='Dartmoor National Park Authority',
        image_url=''
    ),                  
    PublisherStub(
        name='dwi', 
        title='Drinking Water Inspectorate',
        image_url=''
    ),                  
    PublisherStub(
        name='enpa', 
        title='Exmoor National Park Authority',
        image_url=''
    ),                  
    PublisherStub(
        name='ldnpa', 
        title='Lake District National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='nfnpa', 
        title='New Forest National Park Authority',
        image_url=''
    ),                  
    PublisherStub(
        name='nymnpa', 
        title='North York Moors National Park Authority',
        image_url=''
    ),                  
    PublisherStub(
        name='nnpa', 
        title='Northumberland National Park Authority',
        image_url=''
    ),                  
    PublisherStub(
        name='pdnpa', 
        title='Peak District National Park Authority',
        image_url=''
    ),
    PublisherStub(
        name='sdnpa', 
        title='South Downs National Park Authority',
        image_url=''
    ),                  
    PublisherStub(
        name='ukcb', 
        title='UK Co-ordinating Body',
        image_url=''
    ),                  
    PublisherStub(
        name='ydnpa', 
        title='Yorkshire Dales National Park Authority',
        image_url=''
    ),                                                                      
    PublisherStub(
        name='ba', 
        title='Broads Authority',
        image_url=''
    ),                                                                      
    PublisherStub(
        name='cgma', 
        title='Covent Garden Market Authority',
        image_url=''
    ),                                                                              
]
