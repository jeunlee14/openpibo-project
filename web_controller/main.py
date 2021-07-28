import sys
from utils.config import Config as cfg
sys.path.append(cfg.OPENPIBO_PATH + '/edu')
from pibo import Edu_Pibo

from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def sessions():
  return render_template('index.html')

@socketio.on('motion')
def set_motion(motion):
  ret = pibo.set_motion(motion)
  print(ret)

@socketio.on('music')
def audio(music):
  if music == 'stop':
    ret = pibo.stop_audio()
  else:
    ret = pibo.play_audio(cfg.TESTDATA_PATH+music)
  print(ret)

@socketio.on('color')
def neopixel(color):
  r, g, b = map(int, color.split(','))
  ret = pibo.eye_on(r, g, b)
  print(ret)

@socketio.on('speech')
def tts(speech):
  filename = cfg.TESTDATA_PATH+"/tts.mp3"
  ret = pibo.tts(f"<speak>\
              <voice name='WOMAN_READ_CALM'>{speech}<break time='500ms'/></voice>\
            </speak>", filename)
  print(ret)
  ret = pibo.play_audio(filename)
  print(ret)

@socketio.on('camera')
def neopixel(camera):
  if camera == True:
    ret = pibo.start_camera()
  elif camera == False:
    ret = pibo.stop_camera()
  print(ret)

if __name__ == '__main__':
  pibo = Edu_Pibo()
  socketio.run(app, host='0.0.0.0', port=8888, debug=False)
