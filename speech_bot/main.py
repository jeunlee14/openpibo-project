import sys, time
from utils.config import Config as cfg
sys.path.append(cfg.OPENPIBO_PATH + '/edu')
from pibo import Edu_Pibo

sys.path.append(cfg.OPENPIBO_PATH + '/lib')
from scrap.scraplib import Namuwiki, Weather, News

# # sudo pip3 install git+https://github.com/hojp7874/web-scraper.git
# from web_scraper import Namuwiki


def bot_picture(image):
  pibo.draw_image(cfg.TESTDATA_PATH+image)
  pibo.show_display()

def speech(speech_text):
  filename = cfg.TESTDATA_PATH+"/tts.mp3"
  pibo.tts(f"<speak><voice name='WOMAN_READ_CALM'>{speech_text}<break time='1000ms'/></voice></speak>", filename)
  pibo.play_audio(filename, out='local', volume=-1500, background=False)

def wiki_speech():
  speech('어떤 단어에 대해 알고싶으신가요?')
  bot_picture("/icon/mic.png")
  while True:
    # your_input = pibo.stt()['data']
    your_input = input('input: ')
    if 'no result' in your_input:
      speech('잘 못들었어요. 다시 말해주세요.')
      continue

    bot_picture('/icon/check.png')
    try:
      wiki = Namuwiki(your_input)
    except:
      speech(f"{your_input}' 단어는 나무위키에 없어요. 다른 단어를 물어봐주세요.")
      continue
    speech(wiki)
    return

region_table = {
  # '전국': 108,
  '서울': 109,
  '인천': 109,
  '경기': 109,
  '부산': 159,
  '울산': 159,
  '경남': 159,
  '대구': 143,
  '경북': 143,
  '광주': 156,
  '전남': 156,
  '전북': 146,
  '대전': 133,
  '세종': 133,
  '충남': 133,
  '충북': 131,
  '강원': 105,
  '제주': 184
}
def weather_speech():
  # weather = Weather('서울')
  # speech(weather)
  # return
  speech('어느지역 날씨를 알고싶으신가요?')
  while True:
    # your_input = pibo.stt()['data']
    your_input = input('input: ')
    if 'no result' in your_input:
      speech('잘 못들었어요. 다시 말해주세요.')
      continue
    for region in region_table:
      if region in your_input:
        your_input = region
        break
    else:
      speech(f"{your_input}' 지역에 대해서는 잘 모르겠어요. 다른 지역을 말씀해주세요.")
      continue

    weather = Weather(your_input)
    speech(weather)
    speech('도움이 되셨나요?')
    return

def news_speech():
  news = News()
  speech(news)
  return


if __name__ == '__main__':
  pibo = Edu_Pibo()
  while True:
    res = pibo.check_device("system")
    if res['data']['PIR'] == 'person':
      speech('무엇이든지 물어보세요!')
      # your_input = pibo.stt()['data']
      your_input = input('input: ')
      topics = {
        '위키': wiki_speech,
        '날씨': weather_speech,
        '뉴스': news_speech
      }
      for topic, func in topics.items():
        if topic in your_input:
          func()
          break
      else:
        speech('잘 못들었어요.')
    time.sleep(1)