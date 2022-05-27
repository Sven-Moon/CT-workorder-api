
from flask import Blueprint, jsonify, request as r
from app.models import WorkOrder, db
from .services import token_required

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/workorders', methods=['GET'])
def workorders():
    wos = WorkOrder.query.all()
    return jsonify([wo.to_dict() for wo in wos]), 200

@api.route('/workorders/date/created/<string:date>', methods=['GET'])
def workorders_by_order_date(date):
    # test with: 1981-12-15
    wos = WorkOrder.query.filter_by(order_date=date).all()
    return jsonify([wo.to_dict() for wo in wos]), 200

@api.route('/workorders/emp_id/<int:emp_id>', methods=['GET'])
def workorders_by_emp_id(emp_id):
    # test with: 1981-12-15
    wos = WorkOrder.query.filter_by(emp_id=emp_id).all()
    return jsonify([wo.to_dict() for wo in wos]), 200


@api.route('/workorder/<int:wo_num>', methods=['GET'])
def workorder(wo_num):
    wo = WorkOrder.query.filter_by(id=wo_num).first()
    if wo:
        return jsonify(wo.to_dict())
    return jsonify({'error':f'workorder id {wo_num} not found'})



@api.route('/workorder/create', methods=['POST'])
def create_workorder():
    # NOTE TO REVIEWER:
    """When I return the wo_obj.to_dict() after it has been added to 
    the database, it comes back empty. A printout of the WorkOrder object
    before and after the add will look like this:
    <WorkOrder (transient 1901576930784)>
    <WorkOrder 13>
    return value:
    {'created': {}}
    """
    try:
        wo = r.get_json()
        wo_obj = WorkOrder(wo)
    except:
        return jsonify({'error':'malformed request'}),400
    try:
        db.session.add(wo_obj)
        db.session.commit()
    except:
        return jsonify({'error':'couldn\'t add'}),400
    # print(jsonify({'created':wo_obj.to_dict()}))
    return jsonify({"created":wo_obj.to_dict()}), 200



@api.route('/workorder/update/<int:wo_num>', methods=['POST', 'PUT', ])
def update_workorder(wo_num):
    wo = WorkOrder.query.get(wo_num)
    print(type(wo))
    if not wo:
        return jsonify({'error': f'workorder id: {wo_num} not found'})
    wo_new = r.get_json()
    wo.update(wo_new)
    db.session.commit()
    
    return jsonify({'updated': wo.to_dict()})


@api.route('/animals', methods=['GET'])
def get_animals():
    
    return jsonify([a.to_dict() for a in WorkOrder.query.all()]), 200
    return jsonify({a.species: a.to_dict() for a in WorkOrder.query.all()}), 200

@api.route('/workorder/delete/<int:wo_num>', methods=['DELETE'])
def delete_workorder(wo_num):
    wo = WorkOrder.query.get(wo_num)
    new_values = r.get_json()
    if wo: 
        db.session.put(WorkOrder)
        db.session.commit()
        return jsonify({'workorder deleted': wo_num})
    return jsonify({'error': 'no workorder deleted'}),404

@api.route('/workorder/<int:wo_num>', methods=['put'])
def put_workorder():
    
    
    return jsonify({'key':'value'})