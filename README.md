
# ckanext-defra

-----------------
Running the Tests
-----------------

To run the tests, do::

    nosetests --nologcapture --ckan --with-pylons=test.ini

To run the tests and produce a coverage report, first make sure you have
coverage installed in your virtualenv (``pip install coverage``) then run::

    nosetests --nologcapture --with-pylons=test.ini --with-coverage --cover-package=ckanext.defrareports --cover-inclusive --cover-erase --cover-tests
