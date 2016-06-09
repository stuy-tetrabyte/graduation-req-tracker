#!/bin/bash

# This is a simple script that installs all of the project dependencies onto a
# Ubuntu server. It is recommended that this script is NOT run as root, and a
# password is entered whenever prompted, in order to not interfere with the
# permissions of dependencies, and to give the ownership of files to the current
# user.

# Make sure all the software is up-to-date
sudo apt-get update && sudo apt-get upgrade -y

# Install mysql-server
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo apt-get install python-mysqldb python-dev

mysql -u root -p -e "CREATE USER 'tetrabyte'@'localhost' IDENTIFIED BY 'test';"
mysql -u root -p -e 'CREATE DATABASE coursedb;'
mysql -u root -p -e "GRANT ALL ON coursedb.* TO tetrabyte"

sudo pip install -r req-travis.txt

cd utils
python database_setup.py -c
