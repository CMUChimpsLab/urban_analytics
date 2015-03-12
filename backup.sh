#!/bin/bash

echo $(date)
name=$(date | sed 's/\ /_/g')
pg_dumpall > /data/dbbackup/pg_$name.sql && tar -cvf /data/dbbackup/pg_$name.tar /data/dbbackup/pg_$name.sql && rm -r /data/dbbackup/pg_$name.sql
mongodump --out=/data/dbbackup/$name && tar -cvf /data/dbbackup/$name.tar /data/dbbackup/$name && rm -r /data/dbbackup/$name
echo "removing..."
find /data/dbbackup/ -mtime 3 -exec echo {} \;
find /data/dbbackup/ -mtime 3 -exec rm {} \;
echo $(date)
