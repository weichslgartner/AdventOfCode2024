#!/bin/bash
for file in Python/day*.py
do
    echo ${file}
    time python3 ./${file}
    printf "\n"
done