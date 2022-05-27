from functools import wraps
from flask import jsonify, request
from app.models import User

def token_required(api_route):
  @wraps(api_route)
  def decorator_function(*args, **kwargs):
      token = request.headers.get('access-token')
      # can also request username to verify token presented belongs to right user
      if not token:
          return jsonify({
              'Access denied': 'No API token, please register to receive your API token'}), 401
      if not User.query.filter_by(api_token=token).first(): # returns User
          return jsonify({'Access denied': 'Invalid API token'}), 403
          
      return api_route(*args, **kwargs)
  return decorator_function