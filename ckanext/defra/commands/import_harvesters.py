import collections 
import sys
import uuid 
from urlparse import urljoin

import ckan.plugins.toolkit as toolkit


HarvesterStub = collections.namedtuple('HarvesterStub', ['name', 'title', 'url', 'publisher', 'source_type'])


class ImportHarvestersCommand(toolkit.CkanCommand):
    ''' Imports all of the harvesters for Defra (inc. defra) '''
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

        existing_sources = toolkit.get_action('harvest_source_list')(
            self.context, {}
        )
        existing_source_urls = {}
        for source in existing_sources:
            existing_source_urls[source['url'].strip().lower()] = source
        
        print existing_source_urls.keys()
        for harvester in HARVESTERS:
            print 'Checking "{}"'.format(harvester.url)
            harvester_dict = existing_source_urls.get(harvester.url.lower().strip(), {})
            if harvester_dict:
                harvester_dict['owner_org'] = self.publisher_id(harvester.publisher) 
            
            action = 'harvest_source_create'
            harvester_dict = self.harvester_to_dict(harvester)

            toolkit.get_action(action)(
                self.context, harvester_dict
            )

    def publisher_id(self, name):
        res = toolkit.get_action('organization_show')(
            self.context, {"id": name}
        )
        return res['id']
        

    def harvester_to_dict(self, h):
        d= {
            'id': str(uuid.uuid4()),
            'name': h.name, 
            'title': h.title,
            'url': h.url,
            'owner_org': self.publisher_id(h.publisher),
            'source_type': h.source_type
        }
        d['publisher_id'] = d['owner_org']
        return d

HARVESTERS = [
    HarvesterStub(
        name='defra-dsp', 
        title='Defra Metadata harvester',
        url='http://environment.data.gov.uk/discover/defra',
        publisher='defra',
        source_type='csw'
    ),
    HarvesterStub(
        name='forestry-commission-dsp', 
        title='Forestry Commission Metadata harvester',
        url='http://environment.data.gov.uk/discover/fc',
        publisher='forestry-commission',
        source_type='csw'
    ),
    HarvesterStub(
        name='apha-dsp', 
        title='APHA Metadata harvester',
        url='http://environment.data.gov.uk/discover/apha',
        publisher='apha',
        source_type='csw'
    ),
    HarvesterStub(
        name='cefas-dsp', 
        title='Cefas Metadata harvester',
        url='https://cefasapp.cefas.co.uk/api/WAF/data.gov.uk/index.html',
        publisher='cefas',
        source_type='waf'
    ),
    HarvesterStub(
        name='rpa-dsp', 
        title='RPA Metadata harvester',
        url='http://environment.data.gov.uk/discover/rpa',
        publisher='rpa',
        source_type='csw'
    )                    
]
