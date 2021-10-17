#!/bin/bash

cat backup.sql | docker exec -i "$1" /usr/bin/mysql -u root --password="$2" db
