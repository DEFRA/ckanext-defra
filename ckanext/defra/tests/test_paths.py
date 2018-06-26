import ckan.plugins.toolkit as toolkit
import ckanext.defra.plugin as plugin

def test_read_path():
    path = toolkit.url_for('organization_read', id='cabinet-office')
    assert(path == '/organization/cabinet-office')

def test_edit_path():
    path = toolkit.url_for('organization_edit', id='cabinet-office')
    assert(path == '/organization/edit/cabinet-office')

def test_new_read_path():
    path = toolkit.url_for('publisher_read', id='cabinet-office')
    assert(path == '/publisher/cabinet-office')

def test_new_edit_path():
    path = toolkit.url_for('publisher_edit', id='cabinet-office')
    assert(path == '/publisher/edit/cabinet-office')

