from flask import Flask, render_template, redirect, request, flash, url_for
import model

app = Flask(__name__)
app.secret_key = "yaaaayRitchieAndShannon"

@app.route("/", methods=["GET"])
def index():
    #we know this will change
    return render_template("login.html")

@app.route("/", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")

    status = model.authenticate(email, password)
    if status == True:
        flash("User authenticated")
        return redirect(url_for("user_list"))    
    elif status == False:
        flash("Email or Password incorrect, grab your shit umbrella!")
        return redirect(url_for("index"))

@app.route("/register", methods=["GET"])
def registerPage():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def register():
    #get all the things from the forms
    email = request.form.get("email")
    password = request.form.get("password")
    passwordCheck = request.form.get("password_verify")
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
    user_list =  model.Session.query(model.User).limit(5).all()
    return render_template("user_list.html", users= user_list)


if __name__=="__main__":
    app.run(debug=True)