from flask import Flask, render_template, redirect, request, flash, url_for
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list =  model.Session.query(model.User).limit(5).all()
    return render_template("login.html", users=user_list)

@app.route("/", methods=["POST"])
def process_login():
    email = request.form.get("email")
    password = request.form.get("password")

    status = model.authenticate(email, password)
    if status == "SUCCESS":
        flash("User authenticated")
        model.Session['email'] = email
        return redirect(url_for("index"))    
    elif status == "no_user":
        flash("User does not exist")
        return redirect(url_for("index"))
    elif status == "incorrect":
        flash("Email or Password incorrect, grab your shit umbrella!")
        return redirect(url_for("index"))
    
@app.route("/user_list")
def user_list():
    return render_template("user_list.html")


if __name__=="__main__":
    app.run(debug=True)