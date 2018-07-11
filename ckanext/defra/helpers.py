import re
from ckan.plugins.toolkit import _, request, get_action

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
    for extra in pkg['extras']:
        if extra['key'] ==key:
            return extra['value']
    return None

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

    if key in ['release-notes', 'unpublished', 'theme-primary', 'theme-secondary', 'foi-name', 'foi-web', 'access_constraints']:
        return None, None

    if key == 'harvest_source_reference':
        return key, '<a href="{}">{}</a>'.format(value, value)

    if key == 'dataset-reference-date' and value:
        val = ['<dl>']
        blob = json.loads(value)
        for d in blob:
            val.append('<dt>{}</dt>'.format(d['type'].title()))
            val.append('<dd>{}</dd>'.format(d['value']))
        val.append('</dl>')
        return key, ''.join(val)

    if key in ['temporal_coverage-from', 'temporal_coverage-to']:
        b = json.loads(value)
        if b and isinstance(b, list):
            return key, b[0]

    return _(key), value

def is_publisher_show(c):
    return c.action == 'read' and \
        c.controller == 'ckanext.defra.controllers.publisher:PublisherController'

def clean_extra_name(name):
    if name in ['ckan recommended wms preview', 'has views']:
        return None
    names = {
        'id': 'ID',
        'package id': 'Package ID',
        'wms base urls': 'WMS Base URLs'
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

def recent_datasets(count=5):
    results = get_action('package_search')(
        {},
        {
            'sort': 'metadata_created desc',
            'rows': count
        }
    )
    return results['results']
