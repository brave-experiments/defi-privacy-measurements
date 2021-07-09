#!/bin/bash

while IFS=, read -r site type
do
  if [[ "$site" == 'site' ]]; then 
    continue
  fi
  echo "${site}.test"
  node crawler.js $site "data/${site}.csv"
done < sites.csv;
