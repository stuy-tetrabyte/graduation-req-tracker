# graduation-req-tracker
Graduation Requirement Tracker

## Setting up the server

You will need to install a few packages to get this project up and running.

```
sudo apt-get update
sudo apt-get install mysql-server
sudo mysql_secure_installation
sudo apt-get install python-mysqldb
sudo apt-get install python-dev
```

Upon doing `sudo apt-get install mysql-server`, you must enter the password that
the project uses for MySQL. Upon a fresh clone of this repository, this password
will be `test`, though it should be changed if it is for an official deploy.

Upon doing `sudo mysql_secure_installation`, type in your MySQL root password
from earlier:

- Select `n` when asked to change your root password
- `y` when asked to remove anonymous users
- `y` when asked to disable remote access to root
- `y` when asked to remove test database and access to the test database
- `y` when asked to reload the privelege table

Installing other Python requirements:

I originally installed Python Pandas via `pip`, but I ran into a multitude of
issues. The Pandas site suggested that Pandas be installed using anaconda:

```
$ wget http://repo.continuum.io/archive/Anaconda2-4.0.0-Linux-x86_64.sh
$ bash Anaconda2-4.0.0-Linux-x86_64.sh
```

This command will install Pandas, along with a whole bunch of other things.

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
$ mkdir DevBox
$ cd DevBox
$ vagrant init ubuntu/trusty64
$ vagrant up --provider virtualbox
```

Once the VagrantBox is up, do `vagrant ssh` to connect to the box.

To turn off the VagrantBox, do `vagrant halt`.

