from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker

ENGINE = None
Session = None

Base = declarative_base()

### Class declarations go here
# User
# id: integer
# age: integer
# gender: string
# zip_code: string (technically zip codes aren't numeric)
# email: optional string
# password: optional string
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)
    gender = Column(String(10), nullable=True)

# Movie:
# id: integer
# name: string
# released_at: datetime
# imdb_url: string
class Movies(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key = True)
    name = Column(String(64))
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(90), nullable=True)

# Rating:
# id: integer
# movie_id: integer
# user_id: integer
# rating: integer
class Rating(Base):
    __tablename__="rating"
    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer)
    user_id = Column(Integer)
    rating = Column(Integer)

### End class declarations
def createTables():
    #make a funciton to recreate the tables in the db
    Base.metadata.create_all(ENGINE)
    print "all our base are recreated!!!"

def connect():
    global ENGINE
    global Session

    ENGINE = create_engine("sqlite:///ratings.db", echo=True)
    Session = sessionmaker(bind=ENGINE)

    return Session()

def main():
    """In case we need this for something"""
    connect()
    createTables()


if __name__ == "__main__":
    main()
