#!/bin/sh
# script for building the react project

########################
REACT_PROJECT="suicide_chess_react"
BUILD_FOLDER="project/static/react"
########################


# cd into react project
BUILD_FOLDER_REL=../$BUILD_FOLDER
cd $REACT_PROJECT

# run the npm build script
npm install
npm run build

#Remove existing react prod build
rm -rf $BUILD_FOLDER_REL

#Make new react directory
mkdir -p $BUILD_FOLDER_REL

#Move generated react build to new static directory
mv build/static $BUILD_FOLDER_REL

cd $BUILD_FOLDER_REL/static

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
