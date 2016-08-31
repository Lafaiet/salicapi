#!/bin/bash

echo "Stopping services"

/etc/init.d/salic-api stop

echo "Installing SALIC API..."

echo "Installing dependencies:"
apt-get update && apt-get install python-dev python-pip freetds-dev libxml2-dev libxslt1-dev libz-dev
pip install -r salic-api/requirements.txt

echo "Dependencies installed"


echo "Cleaning up..."
rm -r /opt/salic/salic-api/
rm /etc/init.d/salic-api
echo "All cleaned"

echo "Copying files..."
mkdir -p /opt/salic/salic-api/
mkdir /opt/salic/salic-api/log
cp -r salic-api/* /opt/salic/salic-api/
touch /opt/salic/salic-api/log/salic_api.log
cp swagger_specification_PT-BR.json /opt/salic/salic-api/resources/api_doc/
cp startup-script /etc/init.d/salic-api
echo "Done copying..."

chmod +x /etc/init.d/salic-api

echo "SALIC API has been successfuly installed"
echo "Edit the file /opt/salic/salic-api/app/deployment.cfg according to your needs"
