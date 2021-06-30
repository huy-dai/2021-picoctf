#!/bin/bash
#Script to repeatedly unzip files

echo "[+] Starting Script"
echo "[+] Extracting First Doll"
SOURCEDIR=/home/grayhimakar/Documents/2021-picoctf/Forensics/dolls/
cd $SOURCEDIR
unzip -o dolls.jpg #Allow overwrite
FOLDER=./base_images

while [ -d $FOLDER ]
do
    echo "$FOLDER exists on your filesystem."
    cd ./base_images
    unzip -o *
done
echo "Flag found!"
cat flag.txt 