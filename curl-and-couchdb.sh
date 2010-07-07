#!/bin/bash

# curl and couchdb - a love story

set -v
server=http://localhost:5984

# Handshake
curl -s $server
read

# Is something running?
curl -s $server/_active_tasks
read

# List of all databases
curl -s $server/_all_dbs
read

# Readable list of all databases
curl -s $server/_all_dbs | python -m json.tool
read

# View database
curl -s $server/people | python -m json.tool
read

# View all docs
curl -s $server/people/_all_docs | python -m json.tool
read

# View all docs with content
curl -s "$server/people/_all_docs?include_docs=true" | python -m json.tool
read

db=foo
# Create database
curl -s -X PUT $server/$db
read

# Create document
id=$(uuid)
curl -s -d'{"a" : 1, "b" : 2}' -X PUT $server/$db/$id
read

# Get document
curl -s $server/$db/$id | python -m json.tool
read

# Edit document
curl -s $server/$db/$id | python -m json.tool > doc.json
vim doc.json
curl -s -d@doc.json -X PUT $server/$db/$id
curl -s $server/$db/$id | python -m json.tool
read

# Delete it (we need the revision)
rev=$(curl -s $server/$db/$id | egrep -o '[0-9]+-[a-z0-9]{32}')
curl -s -X DELETE "$server/$db/$id?rev=$rev"
read

# Delete the database
curl -s -X DELETE $server/$db
read

# Run a view
curl -s $server/people/_design/people/_view/managers | python -m json.tool
read
