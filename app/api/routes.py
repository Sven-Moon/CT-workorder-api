
from flask import Blueprint, jsonify, request as r
from app.models import WorkOrder, db
from .services import token_required

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/workorders', methods=['GET'])
def workorders():
    wos = WorkOrder.query.all()
    print(wos)
    print([wo.to_dict() for wo in wos])
    return jsonify([wo.to_dict() for wo in wos]), 200








@api.route('/animals', methods=['GET'])
def get_animals():
    
    return jsonify([a.to_dict() for a in WorkOrder.query.all()]), 200
    return jsonify({a.species: a.to_dict() for a in WorkOrder.query.all()}), 200
