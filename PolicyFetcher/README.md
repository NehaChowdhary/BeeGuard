# Policy Fetcher
This module is responsible for fetching policy relevant to an eBPF program and push it in the `/boot/kvstore.txt`. Right now it checks for the keys having `-ve` values in the `kvstore.txt` and updates the proper policy in the same file.
## Build
`sudo docker-compose build`

## Dockerized execution
`sudo docker-compose up -d`
## Standalone Execute
```
watch -n <Interval in Seconds> sudo python3 policyFetcher.py
<Not Implemented yet> sudo python3 policyFetcher.py -p <Interval in Seconds>
```
----------------------------------------------------------------------------------
# SHA256 generator
## Basic Check
```
curl -X POST -F 'file=@README.md' http://localhost:5000/upload
curl -X POST -F 'file=@/home/subhrendu/abc/Dockerfile' http://localhost:5000/upload
cat /boot/kvstore.txt
```