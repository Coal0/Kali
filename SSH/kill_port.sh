#!/bin/bash
pid=$(lsof -i:22 -t);set -f;a=(${pid});
for p in ${a[@]}
do
    kill $p;sleep 1
    if ps -p $p > /dev/null; then kill -9 $p; fi
done
