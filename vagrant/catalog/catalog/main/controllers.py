from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify


main = Blueprint('main', __name__, template_folder = 'templates')


@main.route('/')
def index():
    items = [
    	{
    		"owner" : "Batman",
    		"type"	: "Educational",
    		"cost"	: "3.00"
    	}
    ]

    return render_template("homepage.html", items = items)