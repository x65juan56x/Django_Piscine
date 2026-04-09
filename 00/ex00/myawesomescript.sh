#! /bin/bash

curl -sI "$1" | grep -i "Location:" | cut -d' ' -f2 | tr -d '\r'
