#!/bin/bash

#Running Redis
redis-server &
REDIS_PID=$!


#Activating virtual environment
source ./venv/bin/activate


#Running engine process
python engine.py &
ENGINE_PID=$!

#running flask server
cd ./app
flask run  &
FLASK_SERVER_PID=$!
cd ..

#Cleanup function in case of interrupt
cleanup(){
	echo "Stopping all processes"
	kill  $ENGINE_PID  $FLASK_SERVER_PID  $REDIS_PID  
}

trap cleanup EXIT
wait $REDIS_PID $ENGINE_PID $FLASK_SERVER_PID
