#!/bin/bash
# activate correct conda environment
for file in Python/day*.py
do
    echo ${file}
    time /home/andreas/miniforge3/envs/py312/bin/python ./${file}
    printf "\n"
done