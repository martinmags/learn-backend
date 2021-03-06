from models import Base, User
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
engine = create_engine('sqlite:///usersWithTokens.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@auth.verify_password
def verify_password(username_or_token, password):
  # Try to see if it's a token first
  user_id = User.verify_auth_token(username_or_token)
  if user_id:
    user = session.query(User).filter_by(id=user_id).one()
  else:
    user = session.query(User).filter_by(username=username_or_token).first()
    if not user or not user.verify_password(password):
      return False
  g.user = user
  return True

@app.route('/token')
@auth.login_required
def get_auth_token():
  token = g.user.generate_auth_token()
  return jsonify({'token': token.decode('ascii')})

@app.route('/users', methods=['POST'])
def new_user():
  username = request.json.get('username')
  password = request.json.get('password')
  if username is None or password is None:
    abort(400, "Missing arguments")
  # Existing user
  user = session.query(User).filter_by(username=username).first()
  if user is not None:
    return jsonify({'message':'user already exists'}), 200
  
  user = User(username=username)
  user.hash_password(password)
  session.add(user)
  session.commit()
  return jsonify({ 'username': user.username }), 201

@app.route('/api/users/<int:id>')
def get_user(id):
  user = session.query(User).filter_by(id=id).one()
  if not user:
    abort(400)
  return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
  return jsonify({ 'data':  'Hello {}!'.format(g.user.username) })


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=5000)
  