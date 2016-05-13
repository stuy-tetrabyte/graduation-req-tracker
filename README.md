# graduation-req-tracker
Graduation Requirement Tracker

## Setting up the server

You will need to install a few packages to get this project up and running.

```
sudo pip install pandas xlrd

sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo apt-get install python-mysqldb
```

## Setting up a Vagrant Box for a development environment

To set up a development environment, you will need to install Vagrant and
VirtualBox. On Mac OSX:

```
$ brew install Caskroom/cask/virtualbox
$ brew install Caskroom/cask/vagrant
```

On Ubuntu:

```
$ sudo apt-get update
$ sudo apt-get upgrade
$ sudo apt-get install virtualbox
$ sudo apt-get install vagrant
$ sudo apt-get install virtualbox-dkms
```

After Vagrant and VirtualBox are installed, set up the development box:

```
$ vagrant init ubuntu/trusty64
$ vagrant up --provider virtualbox
```

