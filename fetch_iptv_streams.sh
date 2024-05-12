#!/bin/bash

# Set content type header
echo "Content-type: application/json; charset=utf-8"

# Suppress error reporting
error_reporting=0

# Define URL and keys
url="http://cms.testipmedia.xyz/newtv/itv/index2.php"
specialKey="p2p20210118"
key=$(echo -n $specialKey | md5sum | cut -c1-16)
iv=$(echo -n $specialKey | md5sum | cut -c17-32)

# Generate random device ID
deviceId=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

# Get IP address
Ip=$(curl -s "http://g3.le.com/r?format=1" | awk -F'[/:]' '{print $4}')

# Get IP address from server
getIp=$(curl -s -d "getIP=$deviceId" "$url")

# Construct body data
body='{
    "mac": "5b8a4c0c",
    "model": "HD1910",
    "androidid": "775D2672A66CC2BF37676E9999510BA7",
    "deviceid": "'"$deviceId"'",
    "ip": "'"$Ip"'",
    "app_name": "Focus TV",
    "package_name": "com.newtvbaichuan.iptv",
    "token": "ADA8bC27b3E03AB57E2E15DA9eb8C9",
    "province": ""
}'
compressedBody=$(echo "$body" | gzip -c)

# Encrypt data
enc2=$(echo -n "$compressedBody" | openssl enc -aes-128-cbc -K $key -iv $iv -base64)

# Post encrypted data and get response
res=$(curl -s -d "login=$enc2" "$url")

# Decrypt response
str=$(echo -n "$res" | base64 -d | openssl enc -d -aes-128-cbc -K $key -iv $iv)

# Uncompress and save to file
echo "$str" | gzip -d > orginal.txt

# Process data and save to iptv.txt
json=$(echo "$str" | gzip -d)
categories=$(echo "$json" | jq -r '.data | keys_unsorted[]')

# Write to iptv.txt
rm -f iptv.txt
for category in $categories; do
    if [[ "$category" != "收藏" ]]; then
        echo "$category,#genre#" >> iptv.txt
        channels=$(echo "$json" | jq -r ".data[\"$category\"].channels[] | @tsv" | tr -d '[:space:]')
        while IFS=$'\t' read -r name url; do
            name=$(echo "$name" | tr -d '.')
            echo "$name,$url" >> iptv.txt
        done <<< "$channels"
    fi
done

# Output to stdout
cat iptv.txt
