from flask import render_template, Flask, session, redirect, url_for, escape, request, abort
from app import app

import requests

caturl = "https://www.themealdb.com/api/json/v1/1/categories.php"
response = requests.request("GET", caturl)
categories = response.json()

@app.route('/')
@app.route('/index')
def index():
	content = {
		'title' : "Flask MealDB Demo",
		'text' : "This is a quick demo of Flask using themealdb.com as source data and bootstrap for the theme"
	}
	return render_template('index.html', content=content, cat=categories)


@app.route('/meals/<foodtype>')
def category(foodtype):
	url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=%s" % (foodtype)
	response = requests.request("GET", url)
	items = response.json()
	content = {
		'title' : foodtype,
		'text' : ""
	}
	return render_template('categories.html', content=content, cat=categories, items=items, foodtype=foodtype)

@app.route('/meals/<foodtype>/<dishid>')
def meal(foodtype,dishid):
	url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=%s" % (dishid)
	response = requests.request("GET", url)
	items = response.json()
	content = {
		'title' : items['meals'][0]['strMeal'],
		'text' : items['meals'][0]['strTags']
	}
	return render_template('dish.html', content=content, cat=categories, items=items)
