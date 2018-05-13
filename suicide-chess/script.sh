#!/bin/sh

#Remove existing react prod build
rm -rf static/react

#Make new react directory
mkdir static/react

#Move generated react build to new static directory
mv build/static static/react

cd static/react/static

#Rename default js and css files to comprehensible names
for file in js/*.js
do
  mv "$file" "js/game_compiled.js"
done
for file in css/*.css
do
  mv "$file" "css/game_compiled.css"
done

cd ../..

#Remove files on first level
find . -maxdepth 1 -type f -delete
