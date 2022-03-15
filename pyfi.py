from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import sys
import os
import asyncio
import uvicorn
import threading

app = FastAPI()
last_time = 0

DEBUG_CODE = """
<script>
last_time = {last_time}
  function reload() {
    window.location.reload(true);
  }
  fetch('/changes/'+last_time).then(function(response) { 
    if (response.status == 200) {
      reload();
    }
  });
</script>
"""

@app.get("/")
async def root():
  global last_time
  file = open("index.html", "r")
  content = file.read()
  content = content[: content.find("</body>")] + DEBUG_CODE.format(last_time=last_time) + content[content.find("</body>"):]
  print(content)
  file.close()

  return HTMLResponse(content=content)

@app.get("/changes/{path:path}")
async def changes(path):
  global last_time
  if path < last_time:
    # send 200 as response
    return {'status': 'ok'}
  else: 
    # send 404 as response
    return {'status': 'error'}
  


def listener():
  global last_time
  main_mtime = os.path.getmtime("main.py")
  if main_mtime > last_time:
    # if main.py is modified, reload it
    print("Reloading main.py...")
    # get the current working directory
    cwd = os.getcwd()
    os.system(f"{cwd}/env/Scripts/python.exe main.py")
    print("Reloaded main.py!")
    last_time = main_mtime
  

def set_interval(func, sec):
  def func_wrapper():
      set_interval(func, sec) 
      func()  
  t = threading.Timer(sec, func_wrapper)
  t.start()
  return t

set_interval(listener, 0.1)

# run the server
if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)