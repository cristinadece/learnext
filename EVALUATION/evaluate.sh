#!/bin/bash

FILE=./firenze-merged-sorted
FILE1=./rome-merged-sorted
FILE2=./pisa-merged-sorted

echo "Firenze"
./eval.py ${FILE} 1
./eval.py ${FILE} 2
./eval.py ${FILE} 3
./eval.py ${FILE} 5

echo "Rome"
./eval.py ${FILE1} 1
./eval.py ${FILE1} 2
./eval.py ${FILE1} 3
./eval.py ${FILE1} 5

#echo "Pisa"
#./eval ${FILE} 1
#./eval ${FILE} 2
#./eval ${FILE} 3
#./eval ${FILE} 5
