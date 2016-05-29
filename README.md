#Full Stack Repo

Code for some of my full stack web developer nanodegree projects, each one requires different things to make them functional and are located or will be located below pending completion. *Recommeded to have [vitrual machine](https://www.virtualbox.org/wiki/Downloads) and [vagrant](https://www.vagrantup.com/downloads.html) installed on your computer*

##Tournament Database API Project

This is a project to create a database api for a Swiss system Tournament. Thes steps for setting it up/testing it after are below:

1. Open Terminal/CMD and navigate to the vagrant directory
2. Run `vagrant up`
3. Run `vagrant ssh`
4. Navigate to the **tournament** directory
5. Run `psql -f tournament.sql` to create the db schema
6. Run `python tournament_test.py` to run the test script.
