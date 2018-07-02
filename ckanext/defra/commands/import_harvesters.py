import collections
import sys
import uuid
from urlparse import urljoin

import ckan.plugins.toolkit as toolkit


HarvesterStub = collections.namedtuple('HarvesterStub', ['name', 'title', 'description', 'url', 'publisher', 'source_type'])


class ImportHarvestersCommand(toolkit.CkanCommand):
    ''' Imports all of the harvesters for Defra (inc. defra) from DGU '''
    summary = __doc__.split('\n')[0]
    usage = '\n'.join(__doc__.split('\n')[1:])
    max_args = None
    min_args = 0

    def get_context(self):
        return {
            'ignore_auth': True,
        }

    def command(self):
        self._load_config()

        self.site_url = toolkit.config.get("ckan.site_url")

        existing_sources = toolkit.get_action('harvest_source_list')(
            self.get_context(), {}
        )
        existing_source_urls = {}
        for source in existing_sources:
            existing_source_urls[source['url'].strip().lower()] = source

        print existing_source_urls.keys()
        for harvester in HARVESTERS:
            print 'Checking "{}"'.format(harvester.url)
            action = 'harvest_source_create'

            harvester_dict = existing_source_urls.get(harvester.url.lower().strip())
            if harvester_dict:
                harvester_dict['owner_org'] = self.publisher(harvester.publisher)['id']
                action = 'harvest_source_update'
                del harvester_dict['status']
                del harvester_dict['next_run']
                del harvester_dict['created']
                harvester_dict['source_type'] = harvester_dict['type']
                del harvester_dict['type']
            else:
                harvester_dict = { 'id': str(uuid.uuid4()) }

            self.harvester_to_dict(harvester, harvester_dict)

            toolkit.get_action(action)(
                 self.get_context(), harvester_dict
            )

    def publisher(self, name):
        return toolkit.get_action('organization_show')(
            self.get_context(), {"id": name}
        )

    def harvester_to_dict(self, h, d):
        publisher = self.publisher(h.publisher)
        d.update({
            'name': h.name,
            'title': h.title,
            'url': h.url,
            'owner_org': publisher['id'],
            'source_type': h.source_type,
            'frequency': 'MANUAL',
            'notes': 'Metadata harvester for {}'.format(publisher['title'])
        })
        d['publisher_id'] = d['owner_org']
        return d

HARVESTERS = [
    HarvesterStub(
        name='defra-dsp',
        title='Defra Metadata harvester',
        url='http://environment.data.gov.uk/discover/defra',
        publisher='defra',
        description='',
        source_type='csw'
    ),
    HarvesterStub(
        name='forestry-commission-dsp',
        title='Forestry Commission Metadata harvester',
        url='http://environment.data.gov.uk/discover/fc',
        publisher='forestry-commission',
        description='',        
        source_type='csw'
    ),
    HarvesterStub(
        name='apha-dsp',
        title='APHA Metadata harvester',
        url='http://environment.data.gov.uk/discover/apha',
        publisher='apha',
        description='',        
        source_type='csw'
    ),
    HarvesterStub(
        name='cefas-dsp',
        title='Cefas Metadata harvester',
        url='https://cefasapp.cefas.co.uk/api/WAF/data.gov.uk/index.html',
        publisher='cefas',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='rpa-dsp',
        title='RPA Metadata harvester',
        url='http://environment.data.gov.uk/discover/rpa',
        publisher='rpa',
        description='',        
        source_type='csw'
    ),
    HarvesterStub(
        name='vmd-yearly-financial',
        title='Yearly Financial Dataset',
        url='http://www.vmd.defra.gov.uk/DGU/YearlyFinancialDataset.json',
        publisher='vmd',
        description='',
        source_type='dcat_json'
    ),
    HarvesterStub(
        name='vmd-yearly-calendar',
        title='Yearly Calendar Dataset',
        url='http://www.vmd.defra.gov.uk/DGU/YearlyCalendarDataset.json',
        publisher='vmd',
        description='',        
        source_type='dcat_json'
    ),
    HarvesterStub(
        name='vmd-monthly',
        title='Monthly Dataset',
        url='http://www.vmd.defra.gov.uk/DGU/Monthly.json',
        publisher='vmd',
        description='',        
        source_type='dcat_json'
    ),
    HarvesterStub(
        name='ea-dsp',
        title='EA Metadata harvester',
        url='http://environment.data.gov.uk/discover/ea',
        publisher='ea',
        description='',        
        source_type='csw'
    ),
    HarvesterStub(
        name='jncc-harvester',
        title='JNCC Metadata harvester',
        url='http://data.jncc.gov.uk/waf/',
        publisher='jncc',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='mmo-harvester',
        title='MMO Metadata harvester',
        url='https://s3-eu-west-1.amazonaws.com/inspire-mmo/index.html',
        publisher='mmo',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='ne-dsp',
        title='Natural England Metadata harvester',
        url='http://environment.data.gov.uk/discover/ne',
        publisher='ne',
        description='',        
        source_type='csw'
    ),
    HarvesterStub(
        name='dnpa-harvester',
        title='Dartmoor NPA Metadata harvester',
        url='http://www.dartmoor.gov.uk/visiting/maps/inspire/Inspire.html',
        publisher='dnpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='enpa-harvester',
        title='Exmoor NPA Metadata harvester',
        url='https://locationmde.data.gov.uk/metadata-harvesting/834ef847-25ed-4115-b0df-3901d2be2052/',
        publisher='enpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='ldnpa-harvester',
        title='Lake District NPA Metadata harvester',
        url='https://locationmde.data.gov.uk/metadata-harvesting/e7e7fde7-0a36-46a2-8f05-8b44bcb10ba2/',
        publisher='ldnpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='nfnpa-harvester',
        title='New Forest NPA Metadata harvester',
        url='http://inspire.newforestnpa.gov.uk/index.htm',
        publisher='nfnpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='nymnpa-harvester',
        title='North York Moors NPA Metadata harvester',
        url='https://locationmde.data.gov.uk/metadata-harvesting/5608ab19-4e8e-4d16-b90a-f7382fd9f8d7/',
        publisher='nymnpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='nnpa-harvester',
        title='Northumberland NPA Metadata harvester',
        url='https://locationmde.data.gov.uk/metadata-harvesting/fe3e3673-0345-4851-9747-0f3303870b09/',
        publisher='nnpa',
        description='',
        source_type='waf'
    ),
    HarvesterStub(
        name='pdnpa-harvester',
        title='Peak District NPA Metadata harvester',
        url='http://inspire.misoportal.com/metadata/files/peak_district_national_park',
        publisher='pdnpa',
        description='',
        source_type='waf'
    ),
    HarvesterStub(
        name='sdnpa-harvester-mde',
        title='South Downs NPA Metadata harvester (mde)',
        url='https://locationmde.data.gov.uk/metadata-harvesting/f7794f5a-53f0-4f88-b411-d7e08d0a9d84/',
        publisher='sdnpa',
        description='',
        source_type='waf'
    ),
    HarvesterStub(
        name='sdnpa-harvester-miso',
        title='South Downs NPA Metadata harvester (miso)',
        url='http://inspire.misoportal.com/metadata/files/south_downs_national_park_authority',
        publisher='sdnpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='ydnpa-harvester',
        title='Yorkshire Dales NPA Metadata harvester',
        url='https://locationmde.data.gov.uk/metadata-harvesting/019f74d1-0fc7-46f7-a42f-dd15e059f6a5/',
        publisher='ydnpa',
        description='',        
        source_type='waf'
    ),
    HarvesterStub(
        name='ba-harvester',
        title='Broads Authority Metadata harvester',
        url='https://locationmde.data.gov.uk/metadata-harvesting/4cdb1dfa-c9bc-4ef2-89b3-9fe70512d339/',
        publisher='ba',
        description='',        
        source_type='waf'
    )
]
