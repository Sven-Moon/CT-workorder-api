
from flask import Blueprint, jsonify, request as r
from app.models import Animal, db
from .services import token_required

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/test', methods=['GET'])
def test():
    fox = Animal.query.all()[0]
    return jsonify(fox.to_dict()), 200

@api.route('/animals', methods=['GET'])
def get_animals():
    
    return jsonify([a.to_dict() for a in Animal.query.all()]), 200
    return jsonify({a.species: a.to_dict() for a in Animal.query.all()}), 200

@api.route('/create', methods=['Post'])
@token_required
def create_animal():
    try:
        newdict = r.get_json()
        a = Animal(newdict)
    except:
        return jsonify({'error': 'improper request or body data'}), 400
    try:
        db.session.add(a)
        db.session.commit()
    except:
        return jsonify({'error': 'cannot add: species probably already exists'})
    return jsonify({'created': a.to_dict()}), 200

@api.route('/animal/<string:species>', methods=['GET'])
def get_animal(species):
    
    animal = Animal.query.filter_by(species=species.title()).first()
    if animal:
        return jsonify(animal.to_dict()),200
    return jsonify({'error': f'no such animal exits: {species}'}), 404

@api.route('/update/<string:id>', methods=['POST'])
@token_required
def update_animal(id):
    
    # possible errors: id wrong, data shape wrong
    try:
        newvals = r.get_json()    
        animal = Animal.query.get(id)
        animal.from_dict(newvals)
        db.session.commit()
        return jsonify({'result': f'Updated animal: {animal.to_dict()}'}),200
    except:
        return jsonify({'error':'Invalid request or animal ID doesn\'t exist'})
    
@api.route('/delete/<string:id>', methods=['DELETE'])
@token_required
def delete_animal(id):
    animal = Animal.query.get(id)
    if not animal:
        return jsonify({'error':f'Not found, id: {id}'}), 404
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'Removed animal':animal.to_dict()}), 200