#!/bin/bash

for file in trainset/*; 

do
   for (( i=0; i< 100 ; i++));
   
	do
	#python3 run_target.py  "${file##*/}"  "$i"
	echo "${file##*/}     $i"
        python3 run_target.py  "${file}"  "$i"
       done
done



















