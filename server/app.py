#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        response_body = f'<ul><li>Name: {animal.name}</li>'
        response_body += f'<li>Species: {animal.species}</li>'
        if animal.zookeeper:
            response_body += f'<li>Zookeeper: {animal.zookeeper.name}</li>'
        if animal.enclosure:
            response_body += f'<li>Enclosure: {animal.enclosure.environment}</li>'
        response_body += '</ul>'
        return make_response(response_body, 200)
    else:
        return make_response('<h1>Animal not found</h1>', 404)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        response_body = f'<ul><li>Name: {zookeeper.name}</li>'
        response_body += f'<li>Birthday: {zookeeper.birthday}</li>'
        response_body += '<li>Animals:</li><ul>'
        for animal in zookeeper.animals:
            response_body += f'<li>{animal.name} ({animal.species})</li>'
        response_body += '</ul></ul>'
        return make_response(response_body, 200)
    else:
        return make_response('<h1>Zookeeper not found</h1>', 404)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        response_body = f'<ul><li>Environment: {enclosure.environment}</li>'
        response_body += f'<li>Open to Visitors: {enclosure.open_to_visitors}</li>'
        response_body += '<li>Animals:</li><ul>'
        for animal in enclosure.animals:
            response_body += f'<li>{animal.name} ({animal.species})</li>'
        response_body += '</ul></ul>'
        return make_response(response_body, 200)
    else:
        return make_response('<h1>Enclosure not found</h1>', 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)