import sys
sys.path.append("/home/pi/openpibo-final/lib")

from pibo_device import Pibo_Device
import pibo_extend as pe

motion_db = {
  "앞":"forward1",
  "앞쪽":"forward1",
  "뒤":"backward1",
  "뒤쪽":"backward1",
  "왼쪽":"left1",
  "오른쪽":"right1",
}

class Pibo_Control:
  def __init__(self):
    self.pd = Pibo_Device(self.check_device)
    self.bot_db = {
      "날씨": pe.weather_bot,
      "뉴스": pe.news_bot,
      "일정" : pe.calendar_bot,
      "사진" : self.pd.picture
    }

  def check_device(self, s):
    arr = s.split(':')
    if 'touch' in arr[1]:
      self.pd.display_oled('/home/pi/openpibo-final/bot_icon/pibo_hear.png')
      ret = self.pd.listen(lang='ko-KR')
      if len(ret) > 0:
        self.decode_func(ret[0], voice=True)
        self.pd.display_oled('/home/pi/openpibo-final/bot_icon/pibo_logo_b.png')

  def decode_func(self, string ="오늘 날씨 알려줘", voice=False):
    matched, answer = False, ''
    items = self.pd.analyze_sentence(string)

    for item in items:
      if item[1] == 'NNG':
        for key in self.bot_db.items():
          if key[0] == item[0]:
            answer = self.bot_db[key[0]](string)
            matched = False if answer == None else True
        for key in motion_db:
          if key[0] == item[0]:
            answer = self.pd.motion(motion_db[key[0]])
            matched = False if answer == None else True

    print('match : {}, string : {}'.format(matched, string))
    if matched == False:
      answer = self.pd.chat(string)
    
    self.pd.speak(answer)
    return answer
