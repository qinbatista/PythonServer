#!/bin/bash

trap "kill 0" EXIT

# Run these python scripts from their directory so PATH does not get messed up
python3 ../Application/GameAliya/configuration_manager.py &
sleep 1
python3 ../Application/GameAliya/token_server.py &
python3 ../Application/GameAliya/account_manager.py &
python3 ../Application/GameAliya/game_manager.py &
python3 ../lukseun_server.py &
sleep 1
python3 -m unittest discover . -v &

wait $!
