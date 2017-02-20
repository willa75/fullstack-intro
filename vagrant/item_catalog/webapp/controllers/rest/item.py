import datetime
from flask import abort
from flask_restful import Resource, fields, marshal_with

from webapp.models import db, Item, User, Tag
from .fields import HTMLField
from .parsers import item_get_parser, item_post_parser, item_put_parser

nested_tag_fields = {
    'id': fields.Integer(),
    'title': fields.String()
}

item_fields = {
    'author': fields.String(attribute=lambda x: x.user.username),
    'title': fields.String(),
    'description': fields.String(),
    'price': fields.Float(),
    'tags': fields.List(fields.Nested(nested_tag_fields)),
    'added_date': fields.DateTime(dt_format='iso8601')
}

class ItemApi(Resource):
    @marshal_with(item_fields)
    def get(self, item_id=None):
        if item_id:
            item = Item.query.get(item_id)
            if not item:
                abort(404)

            return item
        else:
            args = item_get_parser.parse_args()
            page = args['page'] or 1

            if args['user']:
                user = User.query.filter_by(
                    username=args['user']
                ).first()
                if not user:
                    abort(404)

                items = user.items.order_by(
                    Item.added_date.desc()
                ).paginate(page, 30)
            else:
                items = Item.query.order_by(
                    Item.added_date.desc()
                ).paginate(page, 30)

            return items.items

    def post(self, item_id=None):
        if item_id:
            abort(400)
        else:
            args = item_post_parser.parse_args(strict=True)

            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)

            new_item = Item(args['title'])
            new_item.date = datetime.datetime.now()
            new_item.description = args['description']
            new_item.price = args['price']
            new_item.user = user

            if args['tag']:
                for item in args['tag']:
                    tag = Tag.query.filter_by(title=item).first()

                    #Add the tag if it exists
                    # If not, make a new tag
                    if tag:
                        new_item.tags.append(tag)
                    else:
                        new_tag = Tag(item)
                        new_item.tags.append(new_tag)

            db.session.add(new_item)
            db.session.commit()
            return new_item.id, 201

    def put(self, item_id=None):
        if not item_id:
            abort(400)
        else:
            item = Item.query.get(item_id)
            if not item:
                abort(404)

            args = item_put_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)
            if user != item.user:
                abort(403)

            if args['title']:
                item.title = args['title']

            if args['description']:
                item.description = args['description']

            if args['price']:
                item.price = args['price']

            if args['tag']:
                for item in args['tag']:
                    tag = Tag.query.filter_by(title=item).first()

                    #Add the tag if it exists
                    # If not, make a new tag
                    if tag:
                        item.tags.append(tag)
                    else:
                        new_tag = Tag(item)
                        item.tags.append(new_tag)

            db.session.add(item)
            db.session.commit()
            return item.id, 201

    def delete(self, item_id=None):
        if not item_id:
            abort(400)
        else:
            item = Item.query.get(item_id)
            if not item:
                abort(404)

            args = item_put_parser.parse_args(strict=True)
            user = User.verify_auth_token(args['token'])
            if not user:
                abort(401)
            if user != item.user:
                abort(403)

            db.session.delete(item)
            db.session.commit()
            return "", 204
