#!/bin/bash
redis-server &
REDIS_PID=$!

source ./venv/bin/activate

python engine.py 
ENGINE_PID=$!

 

cleanup(){
	echo "Stopping all processes"
	Kill ENGINE_PID REDIS_PID
}

trap cleanup EXIT
wait $REDIS_PID $ENGINE_PID
