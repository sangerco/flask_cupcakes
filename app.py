"""Flask app for Cupcakes"""

from flask import Flask, request, render_template, redirect, jsonify
from models import db, connect_db, Cupcake
from forms import AddCupcakeForm

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "doggo"
app.app_context().push()
connect_db(app)


@app.route('/')
def home_page():
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/api/cupcakes')
def list_cupcakes():
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:id>')
def view_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/cupcakes/<int:id>')
def cupcake_page(id):
    cupcake = Cupcake.query.get_or_404(id)
    return render_template('cupcake.html', cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    flavor = request.json['flavor']
    size = request.json['size']
    rating = request.json['rating']
    image = request.json['image']
    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/cupcakes/add', methods=['GET','POST'])
def add_cupcake():

    form = AddCupcakeForm()

    if form.validate_on_submit():
        flavor = request.form['flavor']
        size = request.form['size']
        rating = request.form['rating']
        image = request.form['image']
        new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)
        db.session.add(new_cupcake)
        db.session.commit()
        return redirect('/cupcakes/add')
    else:
        return render_template('add-cupcake.html', form=form)


@app.route('/api/cupcakes/<int:id>', methods=['PATCH'])
def edit_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/cupcakes/<int:id>/edit', methods=['GET', 'POST'])
def edit_cupcake_page(id):
    """ show edit cupcake page, handle incoming data """

    cupcake = Cupcake.query.get_or_404(id)
    form = AddCupcakeForm(obj=cupcake)

    if form.validate_on_submit():
        cupcake.flavor = form.flavor.data
        cupcake.size = form.size.data
        cupcake.rating = form.rating.data
        cupcake.image = form.image.data
        db.session.commit()
        return redirect(f'/cupcakes/{id}')
    else:
        return render_template('edit-cupcake.html', cupcake=cupcake, form=form)


@app.route('/api/cupcakes/<int:id>', methods=['DELETE'])
def delete_cupcake(id):
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = 'deleted')
