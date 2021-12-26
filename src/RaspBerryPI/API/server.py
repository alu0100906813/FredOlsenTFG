
from config import Config
from utils.encrypt import Encrypt
from flask import Flask, render_template, request, session, redirect, Response
from flask_session import Session
import uuid
import datetime

from utils.strings import checkIfIsNotEmpty, deleteSpacesStartEnd
from config import config

app = Flask('Server')
app.secret_key = uuid.uuid4().hex
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

encrypt = Encrypt(config.get('key'))

lastUpdated = datetime.datetime.now()
brokerConnected = False

updatedConfig = False

acceptedConfigValues = [
  'id',
  'ship',
  'host',
  'port',
  'user',
  'password'
]

def updateConfig(newConfig):
  """
  Cuando el usuario actualiza la configuración con nuevos valores
  Esta función se encarga de encriptar la nueva contraseña
  De guardar los valores en la configuración
  Y de en caso de que se haya cambiado el host o el port reiniciar el servidor
  """
  if checkIfIsNotEmpty(newConfig['password']):
    newConfig['password'] = encrypt.encrypt(newConfig['password']) # VER QUE NO ESTÉ EMPTY
  for configValue in newConfig:
    value = deleteSpacesStartEnd(newConfig[configValue])
    if checkIfIsNotEmpty(value) and (configValue in acceptedConfigValues):
      if config.get(configValue) != value: # Solo actualizamos si el valor es diferente, si no, no es diferente
        config.set(configValue, value)
      if configValue == 'host' or configValue == 'port' or configValue == 'id':
        if config.get(configValue) != newConfig[configValue]:
          updatedConfig = True
  config.saveConfig()


@app.route('/')
def index():
  """
  Devuelve el index del panel de control
  En caso de que no esté logueado, pues lo manda al login
  """
  if 'username' in session:
    if session['username'] is not None:
      return render_template('panel.html')
  return redirect('login')


@app.route('/config', methods=['GET'])
def configPanel():
  """
  Devuelve el panel de configuración del IOT. Permite cambiar distintos valores al IOT
  En caso de que el usuario no esté logueado, lo envía a la página de login
  """
  if 'username' in session:
    if session['username'] is not None:
      return render_template('config.html', config = config.getAll(), updated=False)
  return redirect('login')


@app.route('/config', methods=['POST'])
def updateConfigPanel():
  """
  Recibe un post enviado desde la misma página con los nuevos valores de la configuración.
  Actualiza la configuración del IOT. Una vez hecho, reenvia al usuario a la misma página de configuración
  """
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
  """
  Se encarga de mostrar una página al usuario para que pueda acceder al panel
  En caso de que ya se encuentre logeado, pues lo reenvia a la página principal
  """
  if 'username' in session:
    if session['username'] is not None:
      return redirect('/')
  return render_template('login.html')


@app.route('/login', methods=['POST'])
def loginPOST():
  """
  Recibe el POST del login, con las creedenciales introducidas por el usuario
  Comprobamos si estas credenciales son correctas. En cuyo caso, reenviamos al panel
  En caso contrario, volvemos a cargar la página de login
  """
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
  """
  Elimina la sesión del usuario y lo reenvia al index
  """
  session['username'] = None
  return redirect("/")


@app.route('/status', methods=['GET'])
def getStatus():
  """
  Obtiene el estado del broker (Conectado o desconectado)
  Y el número de elementos que quedan en la cola para enviar
  Solo lo envia si el usuario se encuentra logeado, en caso contrario envia un error
  """
  if 'username' in session and session['username'] is not None:
    now = datetime.datetime.now()
    return {'status' : brokerConnected, 'lastUpdate' : (now - lastUpdated).seconds}
  return {'Error' : 'Not logged'}


@app.route('/updateStatus', methods=['POST'])
def updateStatus():
  if request.remote_addr != '127.0.0.1':
    return Response(response='Not Authorized', status=401)
  global brokerConnected
  brokerConnected = request.args.get('status') == 'True'
  lastUpdated = datetime.datetime.now()
  return Response(status=200)


@app.route('/updateConfig', methods=['GET'])
def updateConfig():
  if request.remote_addr != '127.0.0.1':
    return Response(response='Not Authorized', status=401)
  updatedConfig = False
  return {
    'id' : config.get('id'),
    'ship' : config.get('ship'),
    'host' : config.get('host'),
    'port' : config.get('port')
  }  