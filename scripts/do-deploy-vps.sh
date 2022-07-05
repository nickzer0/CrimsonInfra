apikey=`cat "$(dirname "$0")/dokey.txt"`
vps="`od -An -N3 -i < /dev/urandom | sed 's/ *//g' | xargs printf '%x\n'`"
project="crimson"
curl -s -X POST -H "Content-Type: application/json" -H "Authorization: Bearer $apikey" -d '{"name":"'$vps'","region":"lon1","size":"s-1vcpu-1gb","image":"ubuntu-20-04-x64","ssh _keys":[26556575],"backups":false,"ipv6":true,"user_data":null,"private_networking":null,"volumes": null,"tags":["'$project'"]}' "https://api.digitalocean.com/v2/droplets" | jq

