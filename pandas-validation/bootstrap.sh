#!/bin/bash
# Create databases and populate with dummy data
# Note: You might need to set PGUSER environment variable (probably to postgres)

for step in pre post; do
    db=points_${step}
    createdb $db
    psql -f schema.sql $db
done
./populate.py
