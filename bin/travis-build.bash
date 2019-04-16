#!/bin/bash
set -e

echo "This is travis-build.bash..."

echo "Installing the packages that CKAN requires..."
sudo apt-get update -qq
sudo apt-get install solr-jetty

echo "Installing the plugin locally..."
python setup.py develop
pip install -r dev-requirements.txt

echo "Installing CKAN and its Python dependencies..."
git clone https://github.com/ckan/ckan
cd ckan
export latest_ckan_release_branch=ckan-2.8.2
echo "CKAN branch: $latest_ckan_release_branch"
git checkout $latest_ckan_release_branch
pip install --upgrade setuptools
python setup.py develop
pip install -r requirements.txt
pip install -r dev-requirements.txt
cd -

echo "Creating the PostgreSQL user and database..."
sudo -u postgres psql -c "CREATE USER ckan_default WITH PASSWORD 'ckan';"
sudo -u postgres psql -c 'CREATE DATABASE ckan_test WITH OWNER ckan_default;'

echo "SOLR config..."
# Solr is multicore for tests on ckan master, but it's easier to run tests on
# Travis single-core. See https://github.com/ckan/ckan/issues/2972
sed -i -e 's/solr_url.*/solr_url = http:\/\/127.0.0.1:8983\/solr/' test.ini

echo "Installing ckanext-spatial and its Python dependencies..."
git clone https://github.com/ckan/ckanext-spatial
cd ckanext-spatial
python setup.py develop
pip install -r pip-requirements.txt
cd -

echo "Initialising the database..."
paster --plugin=ckan db init -c test.ini

echo "Initialising the harvest plugin"
paster --plugin=ckanext-harvest harvester initdb -c test.ini

echo "Initialising the spatial plugin"
paster --plugin=ckanext-spatial spatial initdb 4326 -c test.ini

echo "Moving test.ini into a subdir..."
mkdir subdir
mv test.ini subdir
mv who.ini subdir

echo "travis-build.bash is done."
