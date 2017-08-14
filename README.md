Java Monit Service in Python
====

## Launch server
```sh
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
bin/start_server.sh
```

## Check java process
```sh
curl -i -X GET http://0.0.0.0:5000/pidfile=<pid file path>
```
