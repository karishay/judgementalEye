from flask import Flask, render_template, redirect, request, flash, url_for, session
import model

app = Flask(__name__)
app.secret_key = "yaaaayRitchieAndShannon"

@app.route("/", methods=["GET"])
def index():
    return render_template("login.html")

@app.route("/", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = hash(request.form.get("password"))

    user = model.authenticate(email, password)
    if user:
        session['user_id'] = user.id
#        sessionUserId = model.Session.query(model.User).get(id)
        return redirect(url_for("getMyRatings"))
    else:
        flash("Email or Password incorrect, grab your shit umbrella!")
        return redirect(url_for("index"))

@app.route("/register", methods=["GET"])
def registerPage():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    #get all the things from the forms
    email = request.form.get("email")
    password = hash(request.form.get("password"))
    passwordCheck = hash(request.form.get("password_verify"))
    age = request.form.get("age")
    zipcode = request.form.get("zipcode")
    gender = request.form.get("gender")

    #check if the passwords match
    if password != passwordCheck:
        flash("Learn how to type better, el suck!")
        return redirect(url_for("registerPage"))

    else:
        if model.checkEmail(email):
            flash("Biotch, you already gots an account.")
            return redirect(url_for("registerPage"))
        else:
            newUser = model.User(email = email, 
                           password = password, 
                           age = age, 
                           zipcode = zipcode, 
                           gender = gender)
            model.Session.add(newUser)
            model.Session.commit()
            return redirect(url_for("index"))


@app.route("/user_list", methods=["GET"])
def user_list():
    user_list =  model.Session.query(model.User).limit(100).all()
    return render_template("user_list.html", users= user_list)

@app.route("/my_ratings", methods=["GET"])
def getMyRatings():
    user_id = session['user_id']
    userObj = model.Session.query(model.User).get(user_id)
    return render_template("ratingsByUser.html", user = userObj)

@app.route("/<int:user_id>/ratings", methods=["GET"])
def getRatings(user_id):
    userObj = model.Session.query(model.User).get(user_id)
    return render_template("ratingsByUser.html", user = userObj)


@app.route("/<int:movie_id>/movies")
def movieRating(movie_id):
    user_id = session.get('user_id', 0)
    userObj = model.Session.query(model.User).get(user_id)

    movieRatings = model.Session.query(model.Movie).get(movie_id)
    movieAverage = model.movieAverage(movieRatings)
    
    return render_template("movies.html", movie = movieRatings, 
                                          movieAverage = movieAverage,
                                          user = userObj)


@app.route("/<int:movie_id>/movies", methods=["POST"])
def saveMovieRating(movie_id):
    user_id = session.get('user_id', 0)
    ratingObject = model.Session.query(model.Rating).filter_by(user_id = user_id, 
                                                               movie_id = movie_id).first()
    if not ratingObject:
        ratingObject = model.Rating(user_id = user_id,
                                    movie_id = movie_id)

    ratingObject.rating = request.form.get("rating")

    model.Session.add(ratingObject)
    model.Session.commit() 
    return redirect(url_for("getMyRatings"))

if __name__=="__main__":
    app.run(debug=True)