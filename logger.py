from flask import *
from utils import get_all_domain_visit, get_all_domain_ip
import os

app = Flask('Logger')

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/icon', methods=["GET"])
def icon():
    return send_file("./asset/no-entry.png", mimetype='image/png')

@app.route('/font/<code>', methods=["GET"])
def font(code):
    return send_file(f"./asset/{code}.woff2", mimetype='font/woff2')

@app.route("/azerty", methods=["GET"])
def dashboard():
    dmlbl, dmvlu = get_all_domain_visit()
    iplbl, ipvlu = get_all_domain_ip()
    # if request.remote_addr in config["dashboard"]:
    return render_template(
        "dashboard.html", 
        nbVisitByDomainLabels=str(dmlbl), 
        nbVisitByDomainValues=str(dmvlu), 
        nbVisitUnauthorizedByIPLabels=str(iplbl), 
        nbVisitUnauthorizedByIPValues=str(ipvlu))
    # else:
    #     return redirect("/", code=301)
    
@app.route("/log/add", methods=["POST"])
def add():
    data = eval(request.data.decode("utf8"))
    open("./data/" + data["ip"] + ".log", "a", encoding="utf8").write(f"{data['timestamp']};{data['domain']};{data['url']}\n")
    return "", 200

def start():
    app.run(host='127.0.0.1', port=5432)#, ssl_context="adhoc")
