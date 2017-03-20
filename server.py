from flask import Flask, render_template,request,redirect,url_for,abort,jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy.orm.exc as exc
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

# Show all the restaurants
@app.route('/')
def ShowRest():
    allrest = session.query(Restaurant).all()
    output = render_template('restaurant.html',rests=allrest)
    return output

# Edit the Restaurant Name
@app.route('/edit/<int:restid>',methods=['GET','POST'])
def EditRestaurant(restid):
    try:
        restname = session.query(Restaurant).filter_by(id=restid).one()
    except exc.NoResultFound:
        abort(404)
    if request.method == 'POST':
        restname.name=request.form['name']
        session.add(restname)
        session.commit()
        return redirect(url_for('ShowRest'))
    else:
        output = '<html><body>'
        output+= '<form action='+url_for('EditRestaurant',restid=restid)+' method="POST">'
        output+= '<p>Restaurant name:'
        output+= '<input type="text" size="30" name="name" value="'+restname.name+'" required>'
        output+= '<input type="submit" value="Save">'
        output+= '</p></body></html>'
    return output

# Create a new Menu Item
@app.route('/restaurant/<int:rest_id>/new',methods=['GET','POST'])
def newMenuItem(rest_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'],
            course = request.form['course'],
            description = request.form['description'],
            price = request.form['price'],
            restaurant_id=rest_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('ShowMenu',restid=rest_id))
    else:
        return render_template('newmenu.html',restid=rest_id,
            menuname='',coursename='',price='',desc='')

# Edit a Menu Item
@app.route('/restaurant/<int:rest_id>/menu/<int:menu_id>/edit',\
    methods=['GET','POST'])
def editMenuItem(rest_id,menu_id):
    if request.method == 'POST':
        try:
            item = session.query(MenuItem).filter_by(id=menu_id).one()
        except exc.NoResultFound:
            abort(404)
        item.name = request.form['name']
        item.course = request.form['course']
        item.description = request.form['description']
        item.price = request.form['price']
        session.add(item)
        session.commit()
        return redirect(url_for('ShowMenu',restid=rest_id))
    else:
        try:
            menu=session.query(MenuItem).filter_by(id=menu_id).one()
        except exc.NoResultFound:
            abort(404)
        return render_template('editmenu.html',restid=rest_id,
            menuid=menu_id,menuname=menu.name,
            coursename=menu.course,price=menu.price,
            desc=menu.description)
@app.route('/delete')
def deleteMenu():
    return "Don't delete, please!"

# Show the menu of a specific restaurant
@app.route('/restaurant/<int:restid>')
def ShowMenu(restid):
    try:
        rest = session.query(Restaurant).filter_by(id=restid).one()
        allmenu = session.query(MenuItem).filter_by(restaurant_id=restid)
    except exc.NoResultFound:
        abort(404)     
    output = render_template('menu.html',restaurant=rest,items=allmenu)
    return output

# Show menu items for a restaurant in JSON format
@app.route('/restaurant/<int:restaurant_id>/JSON/')
def ShowMenuJSON(restaurant_id):
    try:
        allmenu = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    except exc.NoResultFound:
        return '{"error":"No results found"}'    
    return jsonify(MenuItems=[i.serialize for i in allmenu])

if __name__=='__main__':
    app.debug = False
    app.run(host = '0.0.0.0',port = 80)
