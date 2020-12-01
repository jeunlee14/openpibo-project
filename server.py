import sys
sys.path.append("/home/pi/openpibo-final/lib")

from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
import uvicorn
import base64

from pibo_control import Pibo_Control

templates = Jinja2Templates(directory="templates/")
pibo = None
app = FastAPI()

@app.on_event('startup')
async def startup_event():
  global pibo
  pibo = Pibo_Control()

@app.get("/")
async def main(request: Request):
  img = base64.b64encode(open('/home/pi/openpibo-final/images/background.png', 'rb').read()).decode('utf-8')
  return templates.TemplateResponse('index.html', context={'request': request, 'image': img})

@app.post("/command")
def form_post(request: Request, command: str = Form(...)):
  ret = pibo.decode_func(command)
  if "사진" in command:
    img = base64.b64encode(open('/home/pi/openpibo-final/images/photo.jpg', 'rb').read()).decode('utf-8')
  else:
    img = base64.b64encode(open('/home/pi/openpibo-final/images/background.png', 'rb').read()).decode('utf-8')
    
  return templates.TemplateResponse('index.html', context={'request': request, 'result':ret, 'command':command, 'image': img})

if __name__ =="__main__":
  uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)
