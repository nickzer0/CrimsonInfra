#!/bin/python3

from flask import Flask, render_template, request
from subprocess import *
import ast, json, sys, logging, os, time
from json2html import *
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
log = logging.getLogger('werkzeug')
log.disabled = True
os.system('rm db.sqlite3')


# Database stuff
db = SQLAlchemy(app)
class inf_db(db.Model):
  __tablename__ = 'servers'
  __table_args__ = { 'extend_existing': True }
  type = db.Column(db.String(20))
  id = db.Column(db.String(20), primary_key = True)
  hostname = db.Column(db.String(20))
  ip = db.Column(db.String(20))
  status = db.Column(db.String(20))
db.create_all()

### MAKE ADDING DATA TO THE DB A FUNCTION
@app.route("/")
def main():
  output = check_output('./scripts/do-list-vps.sh').decode('utf-8')
  data = json.loads(output)
  for item in data['droplets']:
    type = "Droplet"
    id = item['id']
    hostname = item['name']
    ip = item['networks']['v4'][1]['ip_address']
    status = item['status']
    server = inf_db(type=type, id=id, hostname=hostname, ip=ip, status=status)
    db.session.merge(server)
    db.session.commit()
  rows = inf_db.query.all()
  data = json.loads(output)
  return render_template('main.html', rows=rows)

# Modify this route to provision different server types
@app.route("/deploy", methods=['GET',])
def run():
  output = check_output('./scripts/do-deploy-vps.sh', shell=True).decode('utf-8')
  return output


@app.route("/refreshtable")
def refresh_table():
    output = check_output('./scripts/do-list-vps.sh').decode('utf-8')
    data = json.loads(output)
    for item in data['droplets']:
      type = "Droplet"
      id = item['id']
      hostname = item['name']
      ip = item['networks']['v4'][1]['ip_address']
      status = item['status']
      server = inf_db(type=type, id=id, hostname=hostname, ip=ip, status=status)
      db.session.merge(server)
      db.session.commit()
    rows = inf_db.query.all()
    return render_template('table.html', rows=rows)



@app.route("/refreshdropdown")
def refresh_dropdown():
    rows = inf_db.query.all()
    return render_template('dropdown.html', rows=rows)



@app.route("/modify", methods=['POST'])
def action():
  main()
  action = request.form['action']
  idx = request.form['id']
  call(["bash", "./scripts/do-modify-vps.sh", action, idx])
  inf_db.query.filter_by(id=idx).delete()
  db.session.commit()
  time.sleep(15)
  return render_template('main.html')


if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)
