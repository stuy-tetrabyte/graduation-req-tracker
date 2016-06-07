## Setting up a Vagrant Box for a development environment

NOTE THAT THIS SECTION IS FOR DEVELOPMENT ONLY. WHEN DEPLOYING WE DO NOT NEED
THE VIRTUAL ENVIRONMENT

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

The Ubuntu vagrant distribution is out of date. To fix this, download the
correct debian package [here](https://www.vagrantup.com/downloads.html) and run
```
$ cd [download directory]
$ sudo dpkg -i [downloaded package name]
```

After Vagrant and VirtualBox are installed, set up the development box:

```
$ cd DevBox
$ vagrant up --provider virtualbox
```

Once the VagrantBox is up, do `vagrant ssh` to connect to the box.

To turn off the VagrantBox, do `vagrant halt`.

To clone the repository inside the VagrantBox, first install the latest version
of Git:

```
$ sudo apt-add-repository ppa:git-core/ppa
$ sudo apt-get update
$ sudo apt-get install git
$ git clone https://github.com/stuy-tetrabyte/graduation-req-tracker.git
```

Once you have cloned the repository, run the setup instructions for the server.

