def render(app, **kwargs):
  template="""
  <!DOCTYPE html>
  <html>
    <head>
      <title>{title}</title>
    </head>
    <body>
      {root}
    </body>
  </html>
  """
  with open("index.html", "w") as f:
    f.write(template.format(title=kwargs['title'] if 'title' in kwargs else "Hello, pyfi", root=app.render()))

class Pyfi:
  def __init__(self, name ,child="", **kwargs):
    self.name = name
    if isinstance(child, str):
      self.child = child
    elif isinstance(child, Pyfi):
      self.child = child.render()
    else:
      raise TypeError("child must be a string or a Pyfi object")
    self.kwargs = " ".join(f"{k}='{v}'" for k, v in kwargs.items())
  def render(self):
    return f"<{self.name} {self.kwargs}>{self.child}</{self.name}>" 

class p(Pyfi):
  def __init__(self, child="", **kwargs):
    super().__init__("p", child, **kwargs)

class h1(Pyfi):
  def __init__(self, child="", **kwargs):
    super().__init__("h1", child, **kwargs)

class div(Pyfi):
  def __init__(self, child="", **kwargs):
    super().__init__("div", child, **kwargs)

render(h1("Hello Worl!"))