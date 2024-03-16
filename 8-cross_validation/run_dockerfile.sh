#!/bin/bash
dockerfile=$1
image_name="image_${dockerfile}"
docker build --memory 8g  -t $image_name -f "./${dockerfile}" . && docker run -t --rm $image_name
echo $?
