#!/bin/bash

trap "kill 0" EXIT

# Run these python scripts from their directory so PATH does not get messed up
cd ../Application/GameAliya
python3 configuration_manager.py &
sleep 1
python3 account_manager.py &
python3 game_manager.py &

cd ../../
python3 ../lukseun_server.py &

cd unittests
sleep 1
python3 -m unittest discover . -v &

wait $!

