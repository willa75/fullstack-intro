import datetime
import os
import random
from flask_script import Manager, Server

from webapp import create_app
from webapp.models import db, User, Item, Tag, Role

#default to dev config
env = os.environ.get('WEBAPP_ENV', 'dev')
app = create_app('webapp.config.%sConfig' % env.capitalize())

manager = Manager(app)

manager.add_command("server", Server())

@manager.shell
def make_shell_context():
	return dict(app=app, db=db, User=User, Item=Item, Tag=Tag, Role=Role)

@manager.command
def setup_db():
	'Code to setup initial db with necessary info'
	db.create_all()

	admin_role = Role("admin")
	admin_role.description = "admin of applicaiton"
	db.session.add(admin_role)

	poster_role = Role("poster")
	poster_role.description = "user with ability to post items"
	db.session.add(poster_role)

	admin = User("admin") 
	admin.set_password("password")
	admin.roles.append(admin_role)
	admin.roles.append(poster_role)
	db.session.add(admin)

	tag_one = Tag('clothes')
	tag_two = Tag('books')
	tag_three = Tag('technology')
	tag_four = Tag('sports')
	tag_five = Tag('music')
	tag_list = [tag_one, tag_two, tag_three, tag_four, tag_five]

	s = "Description text"

	for i in xrange(100):
		new_item = Item("Item {}".format(i))
		new_item.user = admin
		new_item.added_date = datetime.datetime.now()
		new_item.description = s
		new_item.tags = random.sample(
			tag_list,
			random.randint(1, 4)
		)
		db.session.add(new_item)

	db.session.commit()


if __name__ == "__main__":
    manager.run()