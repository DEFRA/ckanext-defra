#!/usr/bin/env sh

/usr/lib/ckan/default/bin/nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.defra --cover-inclusive --cover-erase --cover-tests ckanext.defra.tests
