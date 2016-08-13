from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask import current_app as app


main = Blueprint('main', __name__, template_folder = 'templates')


@main.route('/')
def index():
    newItem = Item( name = "test")
    db.session.add(newItem)
    db.session.commit()
    items = [item for item in Item.query.all()]

    return render_template("homepage.html", items = items)