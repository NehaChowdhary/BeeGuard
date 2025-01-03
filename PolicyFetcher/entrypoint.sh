#!/bin/bash
###########################
nohup python3 /app/sha256Gen.py &
###########################
while true; do
    python3 /app/policyFetcher.py
    sleep 10
done

