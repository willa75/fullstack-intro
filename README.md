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

##Item Catalog VM version Repo

This is code used for the udacity item catalog nanodegree, this code has it's own repo which can be viewed [here](https://github.com/willa75/item_catalog)

Code used boilerplate gotten from working through part of [mastering flask](https://www.amazon.com/Mastering-Flask-Jack-Stouffer-ebook/dp/B00YSILB26/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1487435825&sr=1-1&keywords=Mastering+Flask+Mastering+Jack+Stouffer)
An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. To get started with the application follow the steps below:

1. Open Terminal/CMD and navigate to the vagrant directory
2. Run `vagrant up`
3. Run `vagrant ssh`
4. Navigate to the **item_catalog** directory
5. (optional but recommended) Run `virtualenv env`
6. (optional but recommended) Run `source env/bin/activate`
7. Run `export WEBAPP_ENV="dev"`
8. Run `pip install -r requirements.txt` to install the necessary dependencies. If this doesn't work individually install the packages with pip
9. Run `python manage.py setup_db` to create the db schema and close the python shell
8. Run `python manage.py server --host=0.0.0.0` to run the webserver.
9. Open web browser to http://localhost:5000/login to login to the site with credentials:

	username: admin  
	password: password
