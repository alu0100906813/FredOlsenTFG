
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def indexView():
  return '<h1>Hello World</h1>'

@app.route('/login')
def loginView():
  return render_template('login.html')

app.run(port=5000,debug=True)