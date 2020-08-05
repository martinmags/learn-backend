from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Puppy

engine = create_engine('sqlite:///puppies.db', connect_args={'check_same_thread':False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__) 

# Create the appropriate app.route functions. Test and see if they work
# Make an app.route() decorator here for when the client sends the URI "/puppies"

@app.route("/")
@app.route("/puppies", methods=['GET','POST'])
def puppiesFunction():
  if request.method == 'GET':
    return getAllPuppies()  
  elif request.method == 'POST':
    print("Making a new puppy")
    name = request.args.get('name', '')
    description = request.args.get('description','')
    print(name)
    print(description)
    return makeANewPuppy(name, description)
 
#Make another app.route() decorator here that takes in an integer named 'id' for when the client visits a URI like "/puppies/5"
@app.route("/puppies/<int:id>", methods=['GET','PUT', 'DELETE'])
def puppiesFunctionId(id):
  if request.method == 'GET':
    return getPuppy(id)
  elif request.method == 'PUT':
    name = request.args.get('name', '')
    description = request.args.get('description', '')
    return updatePuppy(id,name,description)
  elif request.method == 'DELETE':
    return deletePuppy(id)


def getAllPuppies():
  puppies = session.query(Puppy).all()
  return jsonify(Puppies=[i.serialize for i in puppies])

def getPuppy(id):
  puppy = session.query(Puppy).filter_by(id=id).one()
  return jsonify(Puppy=puppy.serialize)

def makeANewPuppy(name, description):
  puppy = Puppy(name=name, description=description)
  session.add(puppy)
  session.commit()
  return jsonify(Puppy=puppy.serialize)

def updatePuppy(id,name,description):
  puppy = session.query(Puppy).filter_by(id=id).one()
  if not name:
    puppy.name = name
  if not description:
    puppy.description = description
  session.add(puppy)
  session.commit()
  return "Updating a puppy with id {}".format(id)

def deletePuppy(id):
  puppy = session.query(Puppy).filter_by(id=id).one()
  session.delete(puppy)
  session.commit()
  return "Removed a puppy with id {}".format(id)


if __name__ == '__main__':
    app.debug = False
    app.run(host='0.0.0.0', port=5000)	
