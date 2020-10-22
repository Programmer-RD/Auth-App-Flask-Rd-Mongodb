from server import *
from server.db.auth import *
import random


@app.route("/", methods=["POST", "GET"])
def home():
    try:
        urls = [
            "https://digitalsynopsis.com/wp-content/uploads/2015/10/gif-icons-menu-transition-animations-send-mail.gif",
            "https://i.pinimg.com/originals/a2/b7/c8/a2b7c87c0e93b44e9289fafea2aef020.gif",
            "https://i.pinimg.com/originals/77/0c/1e/770c1e178dc59710dc365a7ff1d8a94c.gif",
        ]
        img = random.choice(urls)
        return render_template("home.html", img=img)
    except:
        return abort(404)


@app.route("/Sign/Up", methods=["POST", "GET"])
@app.route("/Sign/Up/", methods=["POST", "GET"])
def sign_up():
    try:
        if "User Name" in session and "Password" in session:
            return redirect("/Sign/In")
        if request.method == "POST":
            user_name = request.form["UN"]
            email = request.form["E"]
            password = request.form["P"]
            su = Sign_Up(user_name=user_name, password=password, email=email)
            result = su.add_to_db()
            print(result)
            if result[0]:
                flash(message=f"{result[1]}", category="success")
                session["User Name"] = user_name
                session["Password"] = password
                return redirect("/Sign/In")
            for x in result[1]:
                flash(message=f"{x}", category="danger")
            return redirect("/Sign/Up")
        else:
            return render_template("sign_up.html")
    except:
        return abort(404)


@app.route("/Sign/In", methods=["POST", "GET"])
@app.route("/Sign/In/", methods=["POST", "GET"])
def sign_in():
    if "User Name" in session and "Password" in session:
        si = Sign_In(
            user_name_or_email=session["User Name"], password=session["Password"]
        )
        result = si.check()
        flash(message=f"{result[1]}", category="success")
        session["Auth"] = True
        session.pop('User Name',None)
        session.pop('Password',None)
        return redirect("/Send/Email(s)")
    if request.method == "POST":
        user_name_or_email = request.form["UNOE"]
        password = request.form["P"]
        si = Sign_In(user_name_or_email=user_name_or_email, password=password)
        result = si.check()
        print(result)
        if result[0]:
            session['Auth'] = True
            flash(message=f"{result[1]}", category="success")
            return redirect('/Send/Email(s)')
        flash(message=f"{result[1]}", category="danger")
        return redirect("/Sign/In")
    else:
        return render_template("sign_in.html")


@app.route("/Send/Email(s)", methods=["POST", "GET"])
@app.route("/Send/Email(s)/", methods=["POST", "GET"])
def send_emails():
    try:
        if "Auth" in session:
            if request.method == "POST":
                to_email = request.form["TE"]
                subject = request.form["S"]
                message = request.form["M"]
                sm = send_mail(to_email=to_email, subject=subject, body=message)
                if sm:
                    flash("Mesasge Sent ! ", "success")
                flash("An Error Occured ! ", "danger")
                return redirect("/Send/Email(s)")
            else:
                return render_template("send_email.html")
        return abort(404)
    except:
        return abort(404)


@app.route("/Log/Out")
def logout():
    try:
        if "Auth" in session:
            session.pop("Auth", None)
            return redirect("/")
        return abort(404)
    except:
        return abort(404)