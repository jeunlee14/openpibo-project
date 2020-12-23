import sys
from utils.config import Config as cfg
sys.path.append(cfg.OPENPIBO_PATH + '/lib')

from speech.speechlib import cSpeech
from speech.speechlib import cDialog
from audio.audiolib import cAudio
from oled.oledlib import cOled
from motion.motionlib import cMotion
from device.devicelib import cDevice
from vision.visionlib import cCamera
from vision.visionlib import cFace
from vision.visionlib import cDetect

class Pibo_Device:
  def __init__(self, func=None):
    self.play_filename = '/home/pi/openpibo-final/data/tts.mp3'
    self.D = cDialog(conf=cfg)
    self.A = cAudio()
    self.O = cOled(conf=cfg)
    self.M = cMotion(conf=cfg)
    self.CA = cCamera()
    self.FA = cFace(conf=cfg)
    self.DT = cDetect(conf=cfg)
    self.T = cSpeech(conf=cfg)
    self.H = cDevice(func).start()
    self.H.send_cmd(self.H.VERSION)
    self.H.send_cmd(self.H.PIR, "on")
    self.display_oled('/home/pi/openpibo-final/bot_icon/pibo_logo_b.png')

  def display_oled(self, filename):
    self.O.draw_image(filename)
    self.O.show()

  def listen(self, lang='ko-KR'):
    return self.T.stt(lang=lang)

  def speak(self, string):
    self.T.tts(string, self.play_filename, 'ko')
    self.A.set_config(volume=-1500)
    self.A.play(self.play_filename)

  def picture(self, string):
    img = self.CA.read()
    ret_img = img.copy()

    datas = self.FA.detect(img)
    for data in datas:
      x,y,w,h = data
      self.CA.rectangle(ret_img, (x,y), (x+w,y+h), color=(30,128,30), tickness=2)

    datas = self.DT.detect_object(img)
    for data in datas:
      x1,y1,x2,y2 = data["position"]
      label = "{}: {:.2f}%".format(data["name"], data["score"])
      self.CA.rectangle(ret_img, (x1,y1), (x2,y2), color=(30,30,128), tickness=2)
      self.CA.putText(ret_img, label, (x1+15, y1+15), size=0.5, color=(128,30,30), tickness=2)

    self.CA.imwrite('/home/pi/openpibo-final/images/photo.jpg', ret_img)
    return "사진촬영했어요"

  def analyze_sentence(self, string):
    return self.D.mecab_pos(string)

  def chat(self, string):
    return self.D.get_dialog(string)

  def motion(self, key):
    self.M.set_motion(key)
    return "움직여보자"
