
from config import Config
from utils.encrypt import Encrypt
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import uuid
from threading import Thread

app = Flask('Server')
app.secret_key = uuid.uuid4().hex
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

config = Config()
encrypt = Encrypt(config.get('key'))

@app.route('/')
def index():
  if 'username' in session:
    if session['username'] is not None:
      return render_template('panel.html')
  return redirect('login')
  
@app.route('/login', methods=['GET'])
def login():
  return render_template('login.html')

@app.route('/login', methods=['POST'])
def loginPOST():
  username = request.form['username']
  password = request.form['password']
  if username and password:
    if username == config.get('user'):
      if encrypt.check(config.get('password'), password):
        session['username'] = username
        return redirect("/")
  return render_template('login.html')

@app.route('/logout')
def logout():
  session['username'] = None
  return redirect("/")

if __name__ == 'server':
  Thread(target=lambda: app.run(port=5000,debug=False, use_reloader=False)).start()