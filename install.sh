#!/bin/bash

echo "Installing SALIC API..."

echo "Installing dependencies:"
apt-get update && apt-get install python-dev python-pip freetds-dev libxml2-dev libxslt1-dev libz-dev
pip install -r salic-api/requirements.txt

echo "Dependencies installed"

cp /opt/salic/salic-api/config.py config.py.old

echo "Cleaning up..."
rm -r /opt/salic/salic-api/
rm /etc/init.d/salic-api
echo "All cleaned"

echo "Copying files..."
mkdir -p /opt/salic/salic-api/
mkdir /opt/salic/salic-api/log
cp -r salic-api/* /opt/salic/salic-api/
cp /opt/salic/salic-api/config_example.py /opt/salic/salic-api/config.py
mv config.py.old /opt/salic/salic-api/
cp startup-script /etc/init.d/salic-api
echo "Done copying..."

chmod +x /etc/init.d/salic-api

echo "SALIC API has been successfuly installed"
echo "Edit the file /opt/salic/salic-api/config.py according to your needs"
echo "If you had an old configuration file, it's saved under /opt/salic/salic-api/config.py.old for your reference"
