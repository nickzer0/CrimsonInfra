#!/bin/bash
apikey=`cat "$(dirname "$0")/dokey.txt"`
project=`cat "$(dirname "$0")/projectname.txt"`
curl -s -X GET -H "Content-Type: application/json" -H "Authorization: Bearer $apikey" "https://api.digitalocean.com/v2/droplets?tag_name=$project"
