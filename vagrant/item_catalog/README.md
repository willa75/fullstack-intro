#Item Catalog Repo

Code for one of my full stack web developer nanodegree projects. *Recommeded to have [virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)*

Code used boilerplate gotten from working through part of [mastering flask](https://www.amazon.com/Mastering-Flask-Jack-Stouffer-ebook/dp/B00YSILB26/ref=sr_1_1?s=digital-text&ie=UTF8&qid=1487435825&sr=1-1&keywords=Mastering+Flask+Mastering+Jack+Stouffer)
An application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items. To get started with the application follow the steps below:

1. Open Terminal/CMD and navigate to the directory of the project
2. (optional but recommended) Run `virtualenv env`
3. (optional but recommended) Run `source env/bin/activate`
4. Run `export WEBAPP_ENV="dev"`
5. Run `git clone https://github.com/willa75/item_catalog.git`
6. Run `pip install -r requirements.txt` to install the necessary dependencies
7. Run `python manage.py setup_db` to create the db schema and close the python shell
8. Run `python manage.py server` to run the webserver and naviagte to the url in the browser.
9. Open web browser to http://localhost:5000/login to login to the site with credentials: 
	username: admin  
	password: password