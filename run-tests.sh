#!/usr/bin/env sh

/usr/lib/ckan/default/bin/nosetests --exe --ckan --reset-db --nologcapture --with-pylons=test.ini $1
