#!/bin/bash

echo $(date)
name=$(date | sed 's/\ /_/g')
mongodump --out=/data/dbbackup/$name && tar -cvf /data/dbbackup/$name.tar /data/dbbackup/$name && rm -r /data/dbbackup/$name
echo "removing..."
find /data/dbbackup/ -mtime 3 -exec echo {} \;
find /data/dbbackup/ -mtime 3 -exec rm {} \;
echo $(date)
