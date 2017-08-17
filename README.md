Java Monit Service in Python
====

## Launch server
```sh
source venv/bin/activate
pip install -r requirements.txt

# run in production mode
bin/start_server.sh

# run in local debug mode
bin/run_local.sh
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

## Server Response
- When all checks pass, status 200 string `AOK` will be returned.
- When any check fails, status 400 and a string message with details about the failure will be returned.

## Check Items
- Deadlock
