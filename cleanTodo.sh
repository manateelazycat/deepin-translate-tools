#!/bin/sh

for finishFile in `ls ./src/finish/`
do 
    find ./src/todo/ -name $finishFile | xargs rm -fv
done    
