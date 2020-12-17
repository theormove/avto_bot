from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import Table
Base = declarative_base()
class Post(Base):
  __tablename__ = 'wp_posts'

  id = Column(Integer, primary_key = True)
  post_excerpt = Column(String)
  ping_status = Column(String)
  post_title = Column(String)
  post_type = Column(String)
  post_status = Column(String)
  guid = Column(String)

  def __init__(self, id, post_excerpt):
    self.id = id
    self.post_excerpt = post_excerpt
    self.ping_status = ping_status
    self.post_title = post_title
    self.post_type = post_type
    self.guid = guid 

class PostMeta(Base):
  __tablename__ = 'wp_postmeta'

  meta_id = Column(Integer, primary_key = True)
  post_id = Column(Integer)
  meta_key = Column(String)
  meta_value = Column(String)

  def __init__(self):
    self.meta_id = meta_id
    self.post_id = post_id
    self.meta_key = meta_key
    self.meta_value = meta_value


class TermRelationship(Base):
  __tablename__ = 'wp_term_relationships'

  object_id = Column(Integer, primary_key = True)
  term_taxonomy_id = Column(Integer)

  def __init__(self):
    self.object_id = object_id 
    self.term_taxonomy_id = term_taxonomy_id

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, primary_key = True)
  first_name = Column(String(20))
  last_name = Column(String(20))
  username = Column(String(15))
  phone_number = Column(String(15))
  registration_date = Column(DateTime)
  def __init__(self, id, registration_date,  first_name = '', last_name = '', username = '', phone_number = ''):
    self.id = id
    self.first_name = first_name
    self.last_name = last_name
    self.username = username
    self.phone_number = phone_number
    self.registration_date = registration_date

class Message(Base):
  __tablename__ = 'message'
  id = Column(Integer, primary_key = True, autoincrement = True)
  sender_id = Column(Integer)
  date = Column(DateTime)
  text = Column(String(5000))
  message_type = Column(String(15))
  def __init__(self, sender_id, date, text = '', message_type = '' ):
    self.sender_id = sender_id
    self.date = date
    self.text = text
    self.message_type = message_type