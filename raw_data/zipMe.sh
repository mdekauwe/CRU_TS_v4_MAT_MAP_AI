#!/bin/bash

for D in PET PRE TMP
do
    tar -zcvf "$D.tar.gz" $D
done
