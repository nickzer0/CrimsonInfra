#!/bin/bash
action=$1
droplet=$2
apikey=`cat "$(dirname "$0")/dokey.txt"`

# Format to run manually is ./do-mofify-vps.sh <action> <vps-ID>
# Actions are Destroy or Rebuild

if [[ $1 == "Destroy" ]]
then
  curl -X DELETE \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $apikey" \
  "https://api.digitalocean.com/v2/droplets/$2"
elif [[ $1 == "Rebuild" ]]
then
  curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $apikey" \
  -d '{"type":"rebuild","image":"ubuntu-20-04-x64"}' \
  "https://api.digitalocean.com/v2/droplets/$2/actions"
fi
