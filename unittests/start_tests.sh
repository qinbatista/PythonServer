#!/bin/bash

trap "kill 0" EXIT

python ../lukseun_server.py &
python ../Application/GameAliya/token_server.py &
python ../Application/GameAliya/WeaponManager.py &
python ../Application/GameAliya/BagManager.py &

sleep 3

python -m unittest discover . -v &
wait $!

