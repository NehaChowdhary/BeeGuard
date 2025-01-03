curl http://localhost:8181/v1/data/ebpf/allow
echo "Should be :false"
echo "----------------"
curl --location 'http://localhost:8181/v1/data/ebpf/allow' \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
        "funcName": "encap_vlan"
    }
  }'
echo "Should be :true"
echo "----------------"
curl --location 'http://localhost:8181/v1/data/ebpf/allow' \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
        "funcName": "mptm_decap"
    }
  }'
echo "Should be :false"
echo "----------------"
curl --location 'http://localhost:8181/v1/data/ebpf/allow' \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
        "funcName": "mptm_encap"
    }
  }'
echo "Should be :true"
echo "----------------"
echo " Elastic data version"
curl --no-progress-meter -X GET "127.0.0.1:9200/index/_doc/data" | jq -r '._version'