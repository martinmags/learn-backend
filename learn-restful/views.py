from models_user import Base, User
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

engine = create_engine('sqlite:///users.db' , connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

@auth.verify_password
def verify_password(username, password):
  user = session.query(User).filter_by(username=username).first()
  if not user or not user.verify_password(password):
    return False
  g.user = user
  return True

@app.route('/api/users', methods=['POST'])
def new_user():
  username = request.json.get('username')
  password = request.json.get('password')
  if username is None or password is None:
    # Missing Arguments
    abort(400, "missing arguments")
  if session.query(User).filter_by(username=username).first() is not None:
    # Existing user
    user = session.query(User).filter_by(username=username).first()
    return jsonify({'message': 'user already exists'}), 200

  user = User(username=username)
  user.hash_password(password)
  session.add(user)
  session.commit()
  return jsonify({ 'username': user.username }), 201

@app.route('/api/users/<int:id>')
def get_user(id):
  user = session.query(User).filter_by(id=id).one()
  if not user:
    abort(400, 'user does not exist')
  return jsonify({'username': user.username})

@app.route('/api/resource')
@auth.login_required
def get_resource():
  return jsonify({'data': "Hello, {}!".format(g.user.username)})

  
if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=5000)

Base.metadata.bind = engine
DBSession = sessionmaker