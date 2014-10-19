#!/bin/bash

echo $(date)
name=$(date | sed 's/\ /_/g')
mongodump --out=/data/dbbackup/$name && tar -cvf /data/dbbackup/$name.tar /data/dbbackup/$name && rm -r /data/dbbackup/$name
find /data/dbbackup/ -mtime +3 -exec rm -r {} \;
echo $(date)
