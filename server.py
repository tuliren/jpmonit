import flask

from jpmonit import *

app = flask.Flask(__name__)


@app.route('/')
def index():
  return """
<p>
  Welcome to jpmonit
</p>
<p>
  The following APIs are supported:
<ul>
  <li>
    /check_all: check all running Java processes
  </li>
  <li>
    /check_process: check Java processes with the specified names
  </li>
  <li>
    /check_pid: check Java process with a specific PID
  </li>
  <li>
    /check_pidfile: check Java process whose PID is specified in a file
  </li>  
</ul>
</p>
"""


@app.route('/check_all')
def check_all():
  monit_result = Jpmonit(app.logger).check_all()
  return return_result(monit_result)


@app.route('/check_process')
def check_process():
  process = flask.request.args.get('process', '')
  monit_result = Jpmonit(app.logger).check_process(process)
  return return_result(monit_result)


@app.route('/check_pid')
def check_pid():
  pid = flask.request.args.get('pid', '')
  monit_result = Jpmonit(app.logger).check_pid(pid)
  return return_result(monit_result)


@app.route('/check_pidfile')
def check_pidfile():
  pid_file_path = flask.request.args.get('pidfile', '')
  monit_result = Jpmonit(app.logger).check_pidfile(pid_file_path)
  return return_result(monit_result)


def return_result(monit_result):
  if monit_result.is_valid():
    return 'AOK'
  else:
    return flask.make_response(monit_result.get_message(), 400)


# local mode: 127.0.0.1:5000
if __name__ == "__main__":
  app.debug = True
  app.run()
