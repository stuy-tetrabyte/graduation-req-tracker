# graduation-req-tracker
Graduation Requirement Tracker

[![Build Status](https://travis-ci.org/stuy-tetrabyte/graduation-req-tracker.svg?branch=feature-backend)](https://travis-ci.org/stuy-tetrabyte/graduation-req-tracker)

## Setting up the server

There is a script located at `setup.sh`. This will perform all the commands, but
will not handle user prompts. You can run the script with `./setup.sh` and input
the responses to the prompts as shown below.

Upon doing `sudo apt-get install mysql-server`, you must enter the password that
the project uses for MySQL.

Upon doing `sudo mysql_secure_installation`, follow these directions when
prompted:

- Select `n` when asked to change your SQL root password
- `y` when asked to remove anonymous users
- `y` when asked to disable remote access to root
- `y` when asked to remove test database and access to the test database
- `y` when asked to reload the privelege table

When installing Anaconda, you should hit enter to accept the Anaconda terms and
conditions. Press `q` to quit reading the Anaconda terms and conditions.

For all future prompts, enter `yes` and hit enter.

During the installation, it may prompt you to append the path for Anaconda in
your `.bashrc` file. You should answer `yes` to this prompt.

This command will install Pandas, along with a whole bunch of other things,
including `xlrd`, which Pandas uses for opening Excel files. It also installs
Python Flask with all of the dependencies.

After this you should be ready to run the database script

Note that if you do not use bash, the last line of the setup script will fail.
Therefore it is highly recommended to use bash for this project.

## Using the Database Setup Script

There is a database setup script located in the `utils` directory, called
`database_setup.py`. For options, do:

```
$ python database_setup.py -h
```

To load the sample data, do:
```
$ python database_setup.py -l ../sample_data/grad_req.xlsx
```

Keep in mind that this is a rather large operation, inserting 16666 rows of 13
columns each.


