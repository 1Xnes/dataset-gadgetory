#!/bin/bash


#this script takes a name from user and renames all images on current folder to selected name (1), selected name (2) like, i made this for dreambooth 

read -p "Please enter file name (example: my_file): " user_file_name

counter=1

for file in *.jpg *.png *.jpeg; do
    if [ -f "$file" ]; then
        extension="${file##*.}"
        new_name="${user_file_name} ($counter).$extension"
        mv "$file" "$new_name"
        ((counter++))
    fi
done

echo "Renaming complete!"

