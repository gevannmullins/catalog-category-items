''' Flask views for the 6 pages on this website '''

import psycopg2
import random, string

from flask import Flask, request, render_template, redirect, url_for, make_response
from flask import session as login_session

import json

import requests
import httplib2
from oauth2client.client import FlowExchangeError, flow_from_clientsecrets

CLIENT_ID = json.loads(open('client_secret.json', 'r').read())['web']['client_id']

app = Flask(__name__)

from database_setup import Category, Item, User




# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('user_login.html', STATE=state)


# privacy
@app.route('/privacy')
def showPrivacy():
    return render_template('privacy_policy')

# Categories
@app.route('/')
@app.route('/categories/')
# def showCategories():
def showCategories():
    categories = session.query(Category).order_by(asc(Category.name))
    items = session.query(Item).all()
    if 'username' not in login_session:
        return render_template(
            'public_catalog.html',
            categories=categories
        )
    else:
        return render_template('catalog.html', categories=categories, items=items)



# Show Category Items
@app.route('/categories/<int:category_id>/')
@app.route('/categories/<int:category_id>/items/')
def showItems(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    creator = getUserInfo(category.user_id)
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    if ('username' not in login_session or
                creator.id != login_session['user_id']):
        return render_template(
            'items.html',
            items=items,
            category=category,
            creator=creator
        )
    else:
        return render_template(
            'public_items.html',
            items=items,
            category=category,
            creator=creator
        )


# Create a new category
@app.route('/categories/new/', methods=['GET', 'POST'])
def newCategory():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        if request.form['name']:
            newCategory = Category(
                name=request.form['name'], user_id=login_session['user_id'])
            session.add(newCategory)
            flash(
                'New Category %s Successfully Created'
                % newCategory.name
            )
            session.commit()
            return redirect(url_for('showCategories'))
        else:
            flash('Please Complete Name Field')
            return render_template('newCategory.html')
    else:
        return render_template('newCategory.html')


# Edit a categories
@app.route('/categories/<int:category_id>/edit/', methods=['GET', 'POST'])
def editCategory(category_id):
    editedCategory = session.query(
        Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedCategory.user_id != login_session['user_id']:
        return """<script>function myFunction()
                {alert('You are not authorized to edit
                this category. Please create your own
                category in order to edit.');}</script>
                <body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['name']:
            editedCategory.name = request.form['name']
            flash('Successfully edited your Category %s' % editedCategory.name)
            return redirect(url_for('showItems', category_id=category_id))
        else:
            return redirect(url_for(
                'editCategory',
                category_id=category_id)
            )
    else:
        return render_template(
            'editCategory.html',
            category=editedCategory
        )


# Delete a category
@app.route('/categories/<int:category_id>/delete/', methods=['GET', 'POST'])
def deleteCategory(category_id):
    categoryToDelete = session.query(
        Category).filter_by(id=category_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if categoryToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction()
                {alert('You do not have permission to delete this category. Please create your own
                category in order to delete.');}</script>
                <body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(categoryToDelete)
        flash('%s Successfully Deleted' % categoryToDelete.name)
        session.commit()
        return redirect(url_for(
            'showCategories',
            category_id=category_id)
        )
    else:
        return render_template(
            'delete_category.html',
            category=categoryToDelete
        )


# Item Services

# Create a new item
@app.route(
    '/categories/<int:category_id>/items/new/',
    methods=['GET', 'POST']
)
def newItem(category_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        return """<script>function myFunction()
                {alert('You are not authorized to add
                items to this category. Please create
                your own category in order to add items.');
                }</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if (request.form['name'] and request.form['description']):
            newItem = Item(
                name=category.form['name'],
                description=request.form['description'],
                category_id=category_id,
                user_id=category.user_id
            )
            session.add(newItem)
            session.commit()
            flash('New %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showItems', category_id=category_id))
        else:
            flash("Please Complete Form")
            return redirect(url_for('newItem',
                                    category_id=category_id,
                                    category=category))
    else:
        return render_template(
            'new_item.html',
            category_id=category_id,
            category=category
        )


# Edit a item
@app.route(
    '/categories/<int:category_id>/items/<int:item_id>/edit',
    methods=['GET', 'POST']
)
def editItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(Item).filter_by(id=item_id).one()
    category = session.query(Category).filter_by(id=category_id).one()
    if login_session['user_id'] != category.user_id:
        return """<script>function myFunction()
                {alert('You are not authorized to edit
                items to this category. Please create
                your own category in order to edit items.');
                }</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if (request.form['name'] and request.form['description']):
            editedItem.name = request.form['name']
            editedItem.description = request.form['description']
            editedItem.category_id = category.id
            session.add(editedItem)
            session.commit()
            flash('Item Successfully Edited')
            return redirect(url_for('showItems',
                                    category_id=category_id))
        else:
            flash("Do Not Leave Any Blanks")
            return redirect(url_for('editItem',
                                    category_id=category_id,
                                    item_id=item_id,
                                    item=editedItem,
                                    category=category))
    else:
        return render_template(
            'edit_item.html',
            category_id=category_id,
            item_id=item_id,
            item=editedItem,
            category=category
        )


# Delete a item
@app.route(
    '/categories/<int:category_id>/items/<int:item_id>/delete',
    methods=['GET', 'POST']
)
def deleteItem(category_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    category = session.query(Category).filter_by(id=category_id).one()
    itemToDelete = session.query(Item).filter_by(id=item_id).one()
    if login_session['user_id'] != category.user_id:
        return """<script>function myFunction()
                {alert('You are not authorized to delete
                items to this category. Please create
                your own category in order to delete items.')
                ;}</script><body onload='myFunction()''>"""
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Item Successfully Deleted')
        return redirect(url_for('showItems', category_id=category_id))
    else:
        return render_template(
            'deleteItem.html',
            item=itemToDelete,
            category=category
        )



# JSON APIs to view Category Information
@app.route('/categories/<int:category_id>/items/JSON')
def categoryItemJSON(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    items = session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/categories/<int:category_id>/items/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    item = session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=Item.serialize)


@app.route('/categories/JSON')
def categoryJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])




