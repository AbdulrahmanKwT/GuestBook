from flask import Flask, render_template, request, session, redirect, url_for
from datetime import datetime

app = Flask(__name__)
# Needed for sessions (Flask signs the session cookie with this key)
app.secret_key = "dev-secret"  # for class use only

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/sign", methods=["GET", "POST"])
def sign():
    if request.method == "POST":
        name = request.form["name"].strip()
        if name:
            entry = {
                "name": name,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            guestbook = session.get("guestbook", [])
            guestbook.insert(0, entry)      # newest first
            session["guestbook"] = guestbook
        return redirect(url_for("guestbook"))
    return render_template("sign.html")

@app.route("/guestbook")
def guestbook():
    entries = session.get("guestbook", [])
    return render_template("guestbook.html", entries=entries)

@app.route("/clear")
def clear():
    session.pop("guestbook", None)
    return redirect(url_for("guestbook"))

if __name__ == "__main__":
    app.run(debug=True)
