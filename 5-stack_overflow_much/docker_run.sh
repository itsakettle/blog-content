#!/bin/bash
image_name="stack_overflow_much_$1"
docker build -t $image_name -f "./$1" . && docker run -t --rm $image_name
echo $?