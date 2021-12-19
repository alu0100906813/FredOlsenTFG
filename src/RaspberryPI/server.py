
from config import Config
from utils.encrypt import Encrypt
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import uuid
from threading import Thread
from RPIQueue import RPIQueue
from brokerConnector import BrokerConnector
from utils.strings import checkIfIsNotEmpty, deleteSpacesStartEnd

app = Flask('Server')
app.secret_key = uuid.uuid4().hex
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

config = Config()
encrypt = Encrypt(config.get('key'))

acceptedConfigValues = [
  'id',
  'ship',
  'host',
  'port',
  'user',
  'password'
]

def updateConfig(newConfig):
  for configValue in newConfig:
    value = deleteSpacesStartend(newConfig[configValue])
    if checkIfIsNotEmpty(value) and configValue in acceptedConfigValues:
      config.set(configValue, value)

@app.route('/')
def index():
  if 'username' in session:
    if session['username'] is not None:
      return render_template('panel.html')
  return redirect('login')

@app.route('/config', methods=['GET'])
def configPanel():
  if 'username' in session:
    if session['username'] is not None:
      return render_template('config.html', config = config.getAll(), updated=False)
  return redirect('login')

@app.route('/config', methods=['POST'])
def updateConfigPanel():
  if 'username' in session:
    if session['username'] is not None:
      updateConfig({
        'id' : request.form['id'],
        'ship' : request.form['ship'],
        'host' : request.form['host'],
        'port' : request.form['port'],
        'user' : request.form['user'],
        'password' : request.form['password']
      })
  return render_template('config.html', config = config.getAll(), updated=True)
  
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

@app.route('/logout', methods=['GET'])
def logout():
  session['username'] = None
  return redirect("/")

@app.route('/status')
def getStatus():
  if 'username' in session and session['username'] is not None:
    return {'queue' : RPIQueue().getLength(), 'status' : BrokerConnector().brokerIsConnected()}
  return {'Error' : 'Not logged'}

if __name__ == 'server':
  Thread(target=lambda: app.run(port=5000,debug=False, use_reloader=False)).start()