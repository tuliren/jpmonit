import flask
from jpmonit import *

app = flask.Flask(__name__)
monit = Jpmonit(app.logger)

@app.route('/')
def index():
  pid_file_path = flask.request.args.get('pidfile', '')
  app.logger.debug("Input pidfile: {0}".format(pid_file_path))

  monit_result = monit.check_process(pid_file_path)
  if not monit_result.is_valid():
    return flask.make_response(monit_result.get_message(), 400)
  else:
    return 'AOK'

# local mode: 127.0.0.1:5000
if __name__ == "__main__":
  app.debug = True
  app.run()
