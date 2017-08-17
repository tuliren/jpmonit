Java Monit Service in Python
====

## Launch server
```sh
source venv/bin/activate
pip install -r requirements.txt
bin/start_server.sh
```

## Help
```sh
curl -i -X GET http://0.0.0.0:5000/
```

## Check java process
```sh
# All
curl -i -X GET http://0.0.0.0:5000/check_all

# By process name
curl -i -X GET http://0.0.0.0:5000/check_process?process=<process name>

# By pid
curl -i -X GET http://0.0.0.0:5000/check_pid?pid=<pid>

# By pid in a pid file
curl -i -X GET http://0.0.0.0:5000/check_pidfile?pidfile=<pid file path>
```
