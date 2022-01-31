from flask import render_template, url_for, Blueprint, session, redirect, request, jsonify
from datetime import datetime
from json import dumps
import database as db
import time

main = Blueprint("main", __name__)

UNIX_WEEK = 604_800
UNIX_MONTH = 2_592_000
format_time = lambda num: str(datetime.utcfromtimestamp(num - (25200)).strftime("%B"))[:3] + datetime.utcfromtimestamp(num - (25200)).strftime(" %d, %Y")
format_dtime = lambda num: str(datetime.utcfromtimestamp(num- (25200)).strftime("%B"))[:3] + datetime.utcfromtimestamp(num - (25200)).strftime(" %d, %Y, %I:%M %p")


@main.route("/", methods=["GET"])
def index():
    if "user" in session:
        return redirect(url_for("main.reports"))
    return redirect(url_for("main.login"))

@main.route("/logout", methods=["GET", "POST"])
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("main.login"))

@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if db.account_credentials_exist(request.form["username"], request.form["password"]):
            session["user"] = request.form["username"]
        else:
            return render_template("login.html", loggedin=False, flash="Invalid credentials")
    if "user" in session:
        return redirect(url_for("main.reports"))
    return render_template("login.html", loggedin=False)

@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if db.account_name_exists(request.form["username"]):
            return render_template("register.html", flash="Username already exists")
        if db.create_account(request.form["username"], request.form["password"]):
            session["user"] = request.form["username"]
    if "user" in session:
        return redirect(url_for("main.reports"))
    return render_template("register.html", loggedin=False)

@main.route("/form", methods=["GET", "POST"])
def form():
    if not "user" in session:
        return redirect(url_for("main.login"))
    if request.method == "POST":
        valid = False
        for f in request.form:
            if f in db.forms.keys():
                db.log_form(session["user"], f, request.form[f], int(time.time()))
                valid = True
        if valid:
            return redirect(url_for("main.reports"))
    return render_template("form.html", loggedin=True)

@main.route("/reports", methods=["GET"])
def reports():
    if not "user" in session:
        return redirect(url_for("main.login"))
    summary = []
    weekly_report = db.retrieve_logs(session["user"], time.time() - UNIX_WEEK)
    if len(weekly_report):
        summary.append({"data":db.format_logs(weekly_report)[0], "title":"Weekly balance", "subtitle":f"Since {format_time(time.time() - UNIX_WEEK)}", "href" : url_for("main.weekly_reports")})
    monthly_report = db.retrieve_logs(session["user"], time.time() - UNIX_MONTH)
    if len(monthly_report):
        summary.append({"data":db.format_logs(monthly_report)[0], "title":"Monthly balance", "subtitle":f"Since {format_time(time.time() - UNIX_MONTH)}", "href" : url_for("main.monthly_reports")})
    alltime_report = db.retrieve_logs(session["user"])
    if len(alltime_report):
        summary.append({"data":db.format_logs(alltime_report)[0], "title":"All time balance", "subtitle":"&nbsp;", "href" : url_for("main.all_reports")})
    return render_template("reports.html", loggedin=True, summary=dumps({"summary": summary}), summarylen=len(summary))

def _reports(type, frequency):
    if not "user" in session:
        return redirect(url_for("main.login"))
    summary = []
    _time = time.time()
    if not frequency:
        temp = {}
        for i in db.retrieve_logs(session["user"]):
            if i[3] in temp.keys():
                temp[i[3]].append(i)
            else:
                temp[i[3]] = [i]
        for k in sorted(temp.keys(), reverse=True):
            d = db.format_logs(temp[k])
            summary.append({"data": d[0], "count":d[1], "general":d[2], "title":f"{format_dtime(k)}"})
    else:
        try:
            while _time > db.earliest_log(session["user"]):
                d = db.format_logs(db.retrieve_logs(session["user"], _time - frequency))
                summary.append({"data": d[0], "count":d[1], "general":d[2], "title":f"{format_time(_time - frequency)} &rarr; {format_time(_time)}"})
                _time -= frequency
        except:
            return redirect(url_for("main.reports"))
    return render_template("subreports.html", title=f"{type.capitalize()} reports", loggedin=True, summary=dumps({"summary": summary}))

@main.route("/reports/weekly", methods=["GET"])
def weekly_reports():
    return _reports("Weekly", UNIX_WEEK)

@main.route("/reports/monthly", methods=["GET"])
def monthly_reports():
    return _reports("Monthly", UNIX_MONTH)

@main.route("/reports/all", methods=["GET"])
def all_reports():
    return _reports("All", False)

@main.route("/reports/clear", methods=["GET"])
def clear_reports():
    if not "user" in session:
        return redirect(url_for("main.login"))
    db.clear_logs(session["user"])
    return redirect(url_for("main.reports"))
