#!/bin/bash

folder_path="uploads"
days=7

find "$folder_path" -type f -mtime +$days -exec rm -f {} \;
