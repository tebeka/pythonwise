#!/bin/bash

for step in pre post; do
    psql -c 'DELETE FROM points' points_${step}
done
