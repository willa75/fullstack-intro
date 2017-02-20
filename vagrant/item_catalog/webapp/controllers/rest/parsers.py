from flask_restful import reqparse

item_get_parser = reqparse.RequestParser()
item_get_parser.add_argument(
	'page',
	type=int,
	location=['json','args', 'headers'],
	required=False
)

item_get_parser.add_argument(
	'user',
	type=str,
	location=['json', 'args', 'headers']
)

item_post_parser = reqparse.RequestParser()
item_post_parser.add_argument(
	'title',
	type=str,
	required=True,
	help="Title is required"
)

item_post_parser.add_argument(
	'description',
	type=str
)

item_post_parser.add_argument(
	'tag',
	type=str,
	action='append'
)

item_post_parser.add_argument(
	'price',
	type=float,
	required=True,
	help='Price is required'
)

item_post_parser.add_argument(
	'token',
	type=str,
	required=True,
	help='Auth token is required to create items'
)

item_put_parser = reqparse.RequestParser()
item_put_parser.add_argument(
	'token',
	type=str,
	required=True,
	help='Autho token is required to edit items'
)

item_put_parser.add_argument(
	'title',
	type=str
)

item_put_parser.add_argument(
	'description',
	type=str
)

item_put_parser.add_argument(
	'tag',
	type=str,
	action='append'
)

item_put_parser.add_argument(
	'price',
	type=float
)

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True)
user_post_parser.add_argument('password', type=str, required=True)