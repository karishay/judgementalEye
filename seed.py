import model
import csv
import re
import datetime



def load_users(session):
    # open a file
    with open('seed_data/u.user', 'rb') as csvfile:
        # parse a line
        user_file = csv.reader(csvfile, delimiter='|')
        # read a line
        for row in user_file:
            #create a user for each row
            user = model.User(id=int(row[0]), age=int(row[1]), gender=row[2], zipcode=row[4])
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
            id  = int(row[0])
            title = row[1].decode("latin-1")
            title = re.sub("\s\(\d{4}\)$", "", title)
            imdb_url = row[4]
            release_date = row[2]
            if not release_date:
                continue
            release_date = datetime.datetime.strptime(release_date, "%d-%b-%Y")
            # fo_serious_release_date = release_date.toordinal()
            # for_reals_release_date = datetime.date.fromordinal(fo_serious_release_date)
            movie = model.Movie(id=id, title=title, imdb_url=imdb_url, release_date=release_date)
            session.add(movie)
        session.commit()
        print "Yay, it added all the movies to the DB!"
    

def load_ratings(session):
    # use u.data
    with open('seed_data/u.data', 'rb') as csvfile:
        ratings_file = csv.reader(csvfile, delimiter='\t')
        for row in ratings_file:
            ratings = model.Rating(user_id=int(row[0]), movie_id=int(row[1]), rating=int(row[2]))
            session.add(ratings)
        session.commit()
        print "Yay, it added all the ratings to the DB!"


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session) 
    load_movies(session)
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

