import pkg_resources
import re
import json

from ckan.plugins.toolkit import _, request, get_action
import ckan.authz as authz


def get_licence_fields_from_free_text(licence_str):
    '''Using a free text licence (e.g. harvested), this func returns license_id
    and licence extra ready to be saved to the dataset dict. It returns a blank
    licence if it is wholely expressed by the license_id.

    return (license_id, licence)
    '''
    license_id, is_wholely_identified = \
        detect_license_id(licence_str)
    if license_id and is_wholely_identified:
        licence = None
    else:
        licence = licence_str
    return (license_id, licence)


licence_regexes = None


def detect_license_id(licence_str):
    '''Given licence free text, detects if it mentions a known licence.

    :returns (license_id, is_wholely_identified)
    '''
    license_id = ''

    global licence_regexes
    if licence_regexes is None:
        licence_regexes = {}
        licence_regexes['ogl'] = [
            re.compile('open government licen[sc]e', re.IGNORECASE),
            re.compile(r'\b\(ogl\)\b', re.IGNORECASE),
            re.compile(r'\bogl\b', re.IGNORECASE),
            re.compile(r'<?https?\:\/\/www.nationalarchives\.gov\.uk\/doc\/open-government-licence[^\s]*'),
            re.compile(r'<?http\:\/\/www.ordnancesurvey\.co\.uk\/oswebsite\/docs\/licences\/os-opendata-licence.pdf'),  # because it redirects to OGL now
            ]
        licence_regexes['ogl-detritus'] = re.compile(
            r'(%s)' % '|'.join((
                'OGL Terms and Conditions apply',
                r'\bUK\b',
                'v3\.0',
                'v3',
                'version 3',
                'for public sector information',
                'Link to the',
                'Ordnance Survey Open Data Licence',
                'Licence',
                'None',
                'OGLs and agreements explained',
                'In accessing or using this data, you are deemed to have accepted the terms of the',
                'attribution required',
                'Use of data subject to the Terms and Conditions of the OGL',
                'data is free to use for provided the source is acknowledged as specified in said document',
                'Released under the OGL',
                'citation of publisher and online resource required on reuse',
                'conditions',
                'Public data \(Crown Copyright\)',
                '[;\.\-:\(\),]*',
                )), re.IGNORECASE
            )
        licence_regexes['spaces'] = re.compile(r'\s+')
    is_ogl = False
    for ogl_regex in licence_regexes['ogl']:
        licence_str, replacements = ogl_regex.subn('OGL', licence_str)
        if replacements:
            is_ogl = True
    if is_ogl:
        license_id = 'uk-ogl'
        # get rid of phrases that just repeat existing OGL meaning
        licence_str = licence_regexes['ogl-detritus'].sub('', licence_str)
        licence_str = licence_str.replace('OGL', '')
        licence_str = licence_regexes['spaces'].sub(' ', licence_str)
        is_wholely_identified = bool(len(licence_str) < 2)
    else:
        is_wholely_identified = None

    return license_id, is_wholely_identified


def show_small_search_bar(c):
    return hasattr(c, 'action') or request.path.startswith('/dashboard')


def _find_extra(pkg, key):
    if pkg is None:
        return None

    extras = pkg.get('extras', [])
    if isinstance(extras, dict):
        return extras.get(key, None)

    for extra in extras:
        if extra['key'] == key:
            return extra['value']
    return None


def is_private_resource(pkg):
    return _find_extra(pkg, 'private-resources') == "True"

UPDATES = {
    'irregular': 'Ad hoc',
    'not planned': 'Not currently planned',
    'continual': 'Continuously',
    'monthly': 'Monthly',
    'quarterly': 'Quarterly',
    'annually': 'Annually',
    'monthly (supersite)': 'Monthly',
    'unknown': 'Not known',
    'biannually': 'Biannually',
    'as needed': 'As required',
    '0': 'Unknown',
}

def update_frequency(pkg):
    e = _find_extra(pkg, 'update_frequency')
    if not e:
        return e
    return UPDATES.get(e.lower().strip(), 'Unspecified')

def access_constraints(pkg):
    import json

    e = _find_extra(pkg, 'access_constraints')
    if not e:
        return None
    ac = json.loads(e)
    if ac:
        return ac[0]
    return ""


def release_notes(pkg):
    return _find_extra(pkg, 'release-notes')


def clean_extra(extra):
    import json
    key, value = extra

    if key in ['release-notes', 'unpublished', 'theme-primary',
               'theme-secondary', 'foi-name', 'foi-web',
               'access_constraints', 'its-dataset', 'register',
               'sla', 'spatial_harvester', 'private-resources',
               'gdpr', 'reference', 'metadata-date']:
        return None, None

    if key == 'harvest_source_reference':
        return key, '<a href="{}">{}</a>'.format(value, value)

    if key == 'dataset-reference-date' and value:
        val = ['<dl>']
        try:
            blob = json.loads(value)
            for d in blob:
                val.append('<dt>{}</dt>'.format(d['type'].title()))
                val.append('<dd>{}</dd>'.format(d['value']))
            val.append('</dl>')
            return "Dataset reference date", ''.join(val)
        except:
            pass

    if key == 'responsible-party':
        val = ['<dl>']
        try:
            blob = json.loads(value)
            if blob:
                for d in blob:
                    val.append('<dt>{}</dt>'.format(d['name'].title()))
                    val.append('<dd>{}</dd>'.format(','.join(d['roles'])))
                val.append('</dl>')
                return key, ''.join(val)
        except:
            pass

    # FIXME!!!
    if key == 'coupled-resource':
        val = ['<ul class="list-unstyled">']
        try:
            blob = json.loads(value)
            if not blob:
                return 'Coupled Resources', ''
            if blob:
                for d in blob:
                    href_list = d.get('href', [''])
                    title_list = d.get('title', [])
                    if not title_list:
                        title_list = d.get('uuid', [])

                    if not href_list or not title_list:
                        continue

                    href = href_list[0]
                    title = title_list[0]

                    if href:
                        if href.startswith('http'):
                            if href.startswith('http://data.gov.uk'):
                                href = href.replace('http://data.gov.uk', '')

                            link = '<li><a href="{}">{}</a></li>'.format(href,
                                                                         title)
                        else:
                            link = '<li>{} - {}</li>'.format(href, title)
                        val.append(link)
                val.append('</ul>')
                return 'Coupled Resources', ''.join(val)
        except:
            pass

    if key == 'spatial' and value:
        return None, None

    if key in ['temporal_coverage-from', 'temporal_coverage-to', 'licence']:
        try:
            b = json.loads(value)
            if b and isinstance(b, list):
                return key, b[0]
        except:
            pass

    return _(key), value


def is_publisher_show(c):
    controller_name = 'ckanext.defra.controllers.publisher:PublisherController'
    return c.action == 'read' and \
        c.controller == controller_name


def clean_extra_name(name):
    if name in ['ckan recommended wms preview', 'has views']:
        return None

    # TODO: Move these to translations and remove the method
    names = {
        'id': 'ID',
        'package id': 'Package ID',
        'wms base urls': 'WMS Base URLs',
        'geographic_coverage': 'Geographic coverage',
        'update_frequency': 'Update frequency',
        'dcat_publisher_name': 'DCAT Publisher name',
        'dcat_issued': 'DCAT Issue Date',
        'frequency_of_update': 'Update frequency',
        'temporal-extent-begin': 'Temporal extent - beginning',
        'temporal-extent-end': 'Temporal extent - end'
    }
    return names.get(name, name.title())


def popular_datasets(count=5):
    results = get_action('package_search')(
        {},
        {
            'sort': 'views_recent desc',
            'rows': count
        }
    )
    return results['results']


def recently_added_datasets(count=5):
    results = get_action('package_search')(
        {},
        {
            'sort': 'metadata_created desc',
            'rows': count
        }
    )
    return results['results']


def recently_updated_datasets(count=5):
    results = get_action('package_search')(
        {},
        {
            'sort': 'metadata_modified desc',
            'rows': count
        }
    )
    return results['results']


def more_like_this(pkg, count=5):
    from ckan.common import config
    import ckan.plugins.toolkit as toolkit
    from ckan.lib.search.common import make_connection

    solr = make_connection()
    query = 'id:"{}"'.format(pkg['id'])
    fields_to_compare = 'text title notes'
    fields_to_return = 'name title score'

    site_id = config.get('ckan.site_id')
    filter_query = '''
        +site_id:"{}"
        +dataset_type:dataset
        +state:active
        +capacity:public
        '''.format(site_id)

    results = solr.more_like_this(q=query,
                                  mltfl=fields_to_compare,
                                  fl=fields_to_return,
                                  fq=filter_query,
                                  rows=count)

    # we want the dataset objects for each item in docs
    datasets = []
    for record in results.docs:
        context = {}
        toolkit.get_action('package_show')(context, {'id': record['name']})
        datasets.append(context['package'])
    return datasets


def get_resource_name(res):
    if not res:
        return ''

    if res.get('name') == 'Unnamed resource':
        if res.get('url', '').lower().find('/wms') >= 0:
            return 'WMS Service'
        elif res.get('url', '').lower().find('/wfs') >= 0:
            return 'WFS Service'
        elif res.get('description', ''):
            return res['description']
        else:
            f = _get_filename(res.get('url', ''))
            if f:
                return f

    return res.get('name', 'Unnamed resource')


def _get_filename(url):
    return url.split('/')[-1]


def is_reference_dataset(pkg):
    e = _find_extra(pkg, "reference")
    return e and e.lower() == 'true'


def is_gdpr_dataset(pkg):
    e = _find_extra(pkg, "gdpr")
    return e and e.lower() == 'true'


def query_has_bbox(r):
    params = request.environ.get('webob._parsed_query_vars')[0]
    return params.get('ext_bbox', '') != ''


def linked_access_constraints(ac):
    refs = {
        'http://www.ordnancesurvey.co.uk/business-and-government/public-sector/mapping-agreements/inspire-licence.html': 'Inspire Licence',
        'http://www.ordnancesurvey.couk/business-and-government/public-sector/mapping-agreements/inspire-licence.html': 'Inspire Licence',
        'http://www.ordnancesurvey.co.uk/business-and-government/public-sector/mapping-agreements/end-user-licence.html': 'Public Sector Mapping Agreement'
    }

    for k, v in refs.iteritems():
        if k in ac:
            ac = ac.replace(k,
                            '<a href="{}">{}</a><br/>'.format(k, v))
    return ac


def org_private_record_count(org_id):
    # Count all of the packages for this organisation that have some
    # identifiable private flag
    # model.Session
    from ckan import model
    p = model.Session.query(model.Package, model.PackageExtra)\
        .filter(model.Package.owner_org == org_id)\
        .filter(model.Package.type == 'dataset')\
        .filter(model.PackageExtra.package_id == model.Package.id)\
        .filter(model.PackageExtra.key == 'gdpr')\
        .all()

    # Need to join to include extras known to be private indicators
    # q = select([extra]).where(extra.c.package_id == pkg.id)
    if len(p) == 0:
        return 0

    return len(p)


def plural(ch, count):
    if count == 1:
        return ''
    return ch


def item_range(page):
    if page.item_count == 1:
        return "1"
    return "{} - {}".format(page.first_item, page.last_item)


def extras_license(pkg):
    lic = _find_extra(pkg, 'licence')
    if lic is not None:
        try:
            return json.loads(lic)[0]
        except (ValueError, IndexError):
            return None
    return None


def get_contact_email(pkg):
    contact_email = _find_extra(pkg, 'contact-email')
    if contact_email is not None:
        return contact_email
    maintainer_email = pkg.get('maintainer_email')
    if maintainer_email is not None:
        return maintainer_email
    return None


def list_letters():
    return [chr(o) for o in range(ord('a'), ord('z') + 1)]


def get_resource_count():
    from ckan import model
    return model.Session.query(model.Resource).count()


def get_harvester_count():
    return len(get_action('harvest_source_list')({}, {'all': True}))


def is_lucene(query):
    """
    Check if a search query contains lucene syntax
    :param query:
    :return:
    """
    match = re.match(
        r'''
        (\w+:\w+)|  # Field Search (<field>:<value>)
        (\w+\ AND\ \w+)|  # And operator (<x> AND <y>)
        (\w+\ OR\ \w+)|  # Or operator (<x> OR <y>)
        (\w+\ NOT\ \w+)|  # Not operator (NOT <x>)
        (-\w+)  # Exclude operator (-<x>)
        ''',
        query,
        re.X | re.I
    )
    return match is not None


def dataset_issues(dataset):
    """
    Return a list of known issues with the dataset. Requires ckanext-defrareports extension
    :param dataset_id:
    :return:
    """
    try:
        from ckanext.defrareports.lib import quality
    except ImportError:
        return None

    issues = {
        'dataset': [],
        'resource': []
    }
    score, reasons = quality.score_record(dataset)
    for reason in reasons:
        issues['dataset'].append(reason)

    for resource in dataset['resources']:
        if resource.get('link_status') != 'active':
            issues['resource'].append({
                'name': resource.get('name'),
                'url': resource.get('url'),
                'issue': '<a href="{} target="_blank">Linked resource</a> doesn\'t seem to exist'.format(
                    resource['url']
                )
            })

    return issues


def is_sysadmin(user):
    return authz.is_sysadmin(user)


def get_current_version():
    return pkg_resources.require("ckanext-defra")[0].version
