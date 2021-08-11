#!/bin/bash

echo "Generating KGCL operations for $1 $2" 

#todo test whether tmp exists
rm -rf ./diff/tmp/*
rm -rf ./diff/stats/*
#mkdir tmp

#todo test whether $1 and $2 are files
sort $1 >> diff/tmp/left
sort $2 >> diff/tmp/right

comm -23 diff/tmp/left diff/tmp/right >> diff/tmp/deleted
comm -13 diff/tmp/left diff/tmp/right >> diff/tmp/added

#todo run python script to test for kgcl operations
