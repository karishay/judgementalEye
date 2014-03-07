import model
import csv

def load_users(session):
    # open a file
    with open('seed_data/u.user', 'rb') as csvfile:
        # parse a line
        user_file = csv.reader(csvfile, delimiter='|')
        # read a line
        for row in user_file:
            #create a user for each row
            user = model.User(id=row[0], age=row[1], gender=row[2], zipcode=row[4])
            #add the user to the session
            session.add(user)
        #commit the session to the db
        #this is important to do in sections to make it ACID compliant-ish
        session.commit()
        print "Yay, it added all the users to the DB! :)"

def load_movies(session):
    # use u.item
    with open('seed_data/u.item', 'rb') as csvfile:
        movie_file = csv.reader(csvfile, delimiter='|')
        for row in movie_file:
            title = row[1]
            title = title.decode("latin-1")
            print title
            movie = model.Movies(id=row[0], name=title, imdb_url=row[3])
            session.add(movie)
        session.commit()
        print "Yay, it added all the movies to the DB!"
    

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as csvfile:
        ratings_file = csv.reader(csvfile, delimiter='\t')
        for row in ratings_file:
            ratings = model.Rating(user_id=row[0], movie_id=row[1], rating=row[2])
            session.add(ratings)
        session.commit()
        print "Yay, it added all the ratings to the DB!"


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session) 
    #load_movies(session)
    load_ratings(session) 
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
# open a file
# read a line
# parse a line
# create an object
# add the object to a session
# commit
# repeat until done

#Parsing titles (removing year of release) 
#Parsing datetimes

