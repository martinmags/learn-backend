"""
Configuration

Typically the same for every project.
1. Import all modules needed
2. Creates instance of declarative base
3. Create/Connect to database
4. Add tables and columns w/ respective schema
"""
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# corresponds to tables in the db
Base = declarative_base()

# Classes, Tables, Mappers(table schema)
class Restaurant(Base):
  __tablename__ = 'restaurant' 
  name = Column( String(80), nullable=False )
  id = Column( Integer, primary_key=True )
  
class MenuItem(Base):
  __tablename__ = 'menu_item'
  name = Column( String(80), nullable=False)
  id =   Column( Integer, primary_key=True)
  course = Column( String(250) )
  description = Column( String(250) )
  price = Column( String(8) )
  restaurant_id = Column( Integer, ForeignKey('restaurant.id') )
  restaurant = relationship( Restaurant )
  
  @property
  def serialize(self):
    return {
      'name': self.name,
      'id': self.id,
      'course': self.course,
      'price': self.price,
      'description': self.description,
    }

#### insert at the end of file ####
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)