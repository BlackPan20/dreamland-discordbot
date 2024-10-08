from flask import Flask
from threading import Thread
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Bot läuft'

def run():
  app.run(host='0.0.0.0')

def keep_alive():
  t = Thread(target=run)
  t.start()
