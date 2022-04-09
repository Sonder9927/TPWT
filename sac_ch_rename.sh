#! /bin/bash

for dir in `ls -d 20*`
do
  python batch_sacfile_rename.py $dir
  python batch_sacfile_ch.py $dir
done

