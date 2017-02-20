import datetime
from os import path
from flask import Blueprint, redirect, render_template, url_for, session, flash
from flask_login import login_required, current_user
from flask_principal import Permission, UserNeed
from sqlalchemy import func

from webapp.extensions import poster_permission, admin_permission
from webapp.models import db, Item, Tag, User, tags
from webapp.forms import ItemForm

catalog_blueprint = Blueprint(
    'catalog',
    __name__,
    template_folder='../templates/catalog',
    url_prefix="/catalog"
)

def sidebar_data():
    'Gets recent created items and most used tags'
    recent = Item.query.order_by(
        Item.added_date.desc()
    ).limit(5).all()
    top_tags = db.session.query(
        Tag, func.count(tags.c.item_id).label('total')
    ).join(
        tags
    ).group_by(Tag).order_by('total DESC').limit(5).all()

    return recent, top_tags

@catalog_blueprint.route('/')
@catalog_blueprint.route('/<int:page>')
def home(page=1):
    'Renders homepage of site'
    items = Item.query.order_by(
        Item.added_date.desc()
    ).paginate(page, 10)
    recent, top_tags = sidebar_data()

    return render_template(
        'home.html',
        items=items,
        recent=recent,
        top_tags=top_tags
    )

@catalog_blueprint.route('/item/<int:item_id>', methods=['GET'])
def item(item_id):
    'Renders item page by id given'
    item = Item.query.get_or_404(item_id)
    tags = item.tags
    user = User.query.filter_by(id = item.user_id).first_or_404()
    recent, top_tags = sidebar_data()

    return render_template(
        'item.html',
        item=item,
        tags=tags,
        recent=recent,
        top_tags=top_tags,
        user=user
    )

@catalog_blueprint.route('/tag/<string:tag_name>')
def tag(tag_name):
    'List all items created with the supplied tag name'
    tag = Tag.query.filter_by(title = tag_name).first_or_404()
    items = tag.items.order_by(Item.added_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'tag.html',
        tag=tag,
        items=items,
        recent=recent,
        top_tags=top_tags
    )

@catalog_blueprint.route('/user/<string:username>')
def user(username):
    'Loads userpage by unique username'
    user = User.query.filter_by(username=username).first_or_404()
    items = user.items.order_by(Item.added_date.desc()).all()
    recent, top_tags = sidebar_data()

    return render_template(
        'user.html',
        user=user,
        items=items,
        recent=recent,
        top_tags=top_tags
    )

@catalog_blueprint.route('/new', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def new_item():
    'Allows logged in users to create new items'
    form = ItemForm()

    if form.validate_on_submit():
        new_item = Item(form.title.data)
        new_item.description = form.description.data
        new_item.added_date = datetime.datetime.now()
        new_item.price = form.price.data

        if form.tags.data:
            for item in form.tags.data:
                tag = Tag.query.filter_by(title=item).first()

                #Add the tag if it exists
                # If not, make a new tag
                if tag:
                    new_item.tags.append(tag)
                else:
                    new_tag = Tag(item)
                    new_item.tags.append(new_tag)

        new_item.user = User.query.filter_by(
            username=current_user.username
        ).one()

        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('.home'))

    return render_template('new.html', form=form)

@catalog_blueprint.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def edit_item(id):
    'Allows users to edit their own items or the items of others if they are an admin'
    item = Item.query.get_or_404(id)
    permission = Permission(UserNeed(item.user.id))

    # We want admins to be able to edit any item
    if permission.can() or admin_permission.can():
        form = ItemForm()

        if form.validate_on_submit():
            item.title = form.title.data
            item.description = form.description.data
            item.added_date = datetime.datetime.now()

            if form.tags.data:
                item.tags = []
                for tag_val in form.tags.data:
                    tag = Tag.query.filter_by(title=tag_val).first()

                    #Add the tag if it exists
                    # If not, make a new tag
                    if tag:
                        item.tags.append(tag)
                    else:
                        new_tag = Tag(tag_val)
                        item.tags.append(new_tag)
            
            db.session.add(item)
            db.session.commit()

            return redirect(url_for('.item', item_id=item.id))

        # Make sure the tag values are displayed and not the class representations
        tag_title_list = []
        for tag in item.tags:
            tag_title_list.append(str(tag.title))

        tag_title_list = ','.join(tag_title_list)
        return render_template('edit.html', form=form, item=item, tags=tag_title_list)

    abort(403) 

@catalog_blueprint.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
@poster_permission.require(http_exception=403)
def delete_item(id):  
    'Allows users to delete their own items or the items of others if they are an admin'
    item = Item.query.get_or_404(id)
    permission = Permission(UserNeed(item.user.id))

    # We want admins to be able to edit any item
    if permission.can() or admin_permission.can():
        db.session.delete(item)
        db.session.commit()

        flash("The item was successfully deleted", category="success")
        return redirect(url_for('.home'))

    abort(403)