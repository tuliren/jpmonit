import flask

app = flask.Flask(__name__)

@app.route('/')
def index():
  pid_file_path = flask.request.args.get('pidfile', '')
  app.logger.debug("Input pidfile: {0}".format(pid_file_path))

  if not pid_file_path:
    return flask.make_response("Missing pid file path (pidfile)", 400)

  app.logger.debug("Check pid in {0}".format(pid_file_path))
  return "AOK".format(pid_file_path)

# local mode: 127.0.0.1:5000
if __name__ == "__main__":
  app.debug = True
  app.run()
