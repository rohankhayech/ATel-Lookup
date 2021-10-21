#!/bin/bash

docker exec "$1" /usr/bin/mysqldump -u root --password="$2" db > backup.sql
