#!/bin/bash
#
# This script takes as input a file containing one URL per line.  For each URL,
# it runs the request logger and writes its output to DOMAIN.json.

script_dir=$(dirname "$0")
crawler="${script_dir}/run.js"
google_chrome_binary="/opt/google/chrome/google-chrome"
google_chrome_profile="PATH"
metamask_path="PATH"

if [ $# != 1 ]
then
    >&2 echo "Usage: $0 FILE"
    exit 1
fi
file_name="$1"

while read url; do
  echo "Crawling ${url}."
  domain=$(echo "$url" | awk -F/ '{print $3}')
  "$crawler" \
    --interactive \
    --binary "$google_chrome_binary" \
    --profile "$google_chrome_profile" \
    --metamask "$metamask_path" \
    --ancestors \
    --url "$url" > "${domain}.json"
done <"$file_name"
