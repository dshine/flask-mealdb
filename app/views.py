from flask import render_template, Flask, session, redirect, url_for, escape, request, abort
from app import app

from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()

import requests

def checkCache(id, url, hours):
	rv = cache.get(id)
	if rv is None:
		try:
			rv = requests.request("GET", url)
		except requests.exceptions.RequestException as e:
			abort(500)		
		cache.set(id, rv, timeout = hours * 60 * 60)
	return rv

caturl = "https://www.themealdb.com/api/json/v1/1/categories.php"
categories = {}

categories = checkCache( 'categories', caturl, 24).json()

@app.route('/')
@app.route('/index')
def index():
	content = {
		'title' : "Flask MealDB Demo",
		'text' : "This is a quick demo of Flask using the mealdb.com as source data and bootstrap for the theme"
	}
	return render_template('index.html', content=content, cat=categories)


@app.route('/meals/<foodtype>')
def category(foodtype):
	url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=%s" % (foodtype)
	items = checkCache(foodtype,url,12).json()
	content = {
		'title' : foodtype,
		'text' : ""
	}
	return render_template('categories.html', content=content, cat=categories, items=items, foodtype=foodtype)

@app.route('/meals/<foodtype>/<dishid>')
def meal(foodtype,dishid):
	url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=%s" % (dishid.split('-')[0])
	items = checkCache(dishid.split('-')[0],url,48).json()
	content = {
		'title' : items['meals'][0]['strMeal'],
		'text' : items['meals'][0]['strTags']
	}
	return render_template('dish.html', content=content, cat=categories, items=items)

@app.errorhandler(500)
def notFound(error):
	content = {'title': 'Hueston we have a problem'}
	categories = {}
	return render_template('500.html', content=content, cat=categories, error=error), 500

