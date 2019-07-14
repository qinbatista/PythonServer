#!/bin/bash

trap "kill 0" EXIT

python3 ../lukseun_server.py &
python3 ../Application/GameAliya/token_server.py &
python3 ../Application/GameAliya/WeaponManager.py &
python3 ../Application/GameAliya/BagManager.py &

sleep 3

python3 -m unittest discover . -v &
wait $!

