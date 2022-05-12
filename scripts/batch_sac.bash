#! /bin/bash

for dir in `ls -d 20*`
do
  python batch_sac.py $dir
done
