import os
import sys
import base64
sys.path.append("/home/pi/openpibo-project/final/lib")
from pibo_control import Pibo_Control

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def sessions():
  return render_template('index.html')

#def messageReceived(methods=['GET', 'POST']):
#    print()

@socketio.on('command')
def f_command(command, methods=['GET', 'POST']):
  ret = pibo.decode_func(command)
  if "사진" in command:
    img = base64.b64encode(open('/home/pi/openpibo-project/final/images/photo.jpg', 'rb').read()).decode('utf-8')
  else:
    img = base64.b64encode(open('/home/pi/openpibo-project/final/images/background.png', 'rb').read()).decode('utf-8')

  socketio.emit('img', img)
  socketio.emit('result', ret)

if __name__ == '__main__':
  pibo = Pibo_Control()
  socketio.run(app, host='0.0.0.0', port=8888, debug=False)
