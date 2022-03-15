import os
from flask import Flask, Response
import threading

app = Flask(__name__)
last_time = 0

DEBUG_CODE = """
<script>
last_time = %d;
  function reload() {
    fetch(window.location.origin + '/changes/'+last_time).then(function(response) { 
    if (response.status == 200) {
      window.location.reload(true);
    }
  });
  }
  setInterval(reload, 1000);
</script>
"""

@app.get("/")
def root():
  global last_time
  file = open("index.html", "r")
  content = file.read()
  content = content[: content.find("</body>")] + DEBUG_CODE%(last_time) + content[content.find("</body>"):]
  print(content)
  file.close()

  return content

@app.get("/changes/<int:path>")
def changes(path):
  global last_time
  if path < int(last_time):
    # send 200 as response
    print('Sending 200')
    return Response(status=200)
  else: 
    # send 404 as response
    print('Sending 404')
    return Response(status=404)
  


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

t = set_interval(listener, 0.1)

# run the server
if __name__ == "__main__":
  app.run()
  t.cancel()