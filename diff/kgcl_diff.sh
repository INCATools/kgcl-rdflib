#!/bin/bash

echo "Generating KGCL operations for $1 $2" 

#todo test whether tmp exists
mkdir tmp

#todo test whether $1 and $2 are files
sort $1 >> tmp/left
sort $2 >> tmp/right

comm -23 tmp/left tmp/right >> tmp/deleted
comm -13 tmp/left tmp/right >> tmp/added

#todo run python script to test for kgcl operations
