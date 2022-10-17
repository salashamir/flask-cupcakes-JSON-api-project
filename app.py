"""Flask app for Cupcakes"""

from flask import Flask, request, redirect, render_template, flash, url_for, jsonify
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "555667111key"

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# rest json API ROUTES

@app.route('/api/cupcakes')
def retrieve_cupcakes():
    """Return all cupcakes in db
    
    Responds with JSON represetning all cupcakes
    """
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def retrieve_cupcake(cupcake_id):
    """"Returns a specific cupcake as JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Add a cupcake to db and return JSON representing that cupcake"""
    data = request.json
    new_cupcake = Cupcake(flavor=data['flavor'],rating=data['rating'],size=data['size'],image=data['image'] or None)

    db.session.add(new_cupcake)
    db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Update cupcake of cupcake_id and return JSON of updated cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    data = request.json

    cupcake.flavor = data.get('flavor', cupcake.flavor)
    cupcake.rating = data.get('rating', cupcake.rating)
    cupcake.size = data.get('size', cupcake.size)
    cupcake.image = data.get('image', cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Delete cupcake with cupcake_id and return deletion success message JSON"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")

# page ROUTE(S)
@app.route('/')
def home():
    """Returns homepage template which is list of cupcakes and a form to add a new one"""
    return render_template('index.html')
