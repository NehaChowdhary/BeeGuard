# OPA Docker for eBPF Verification
```
├── opa_linux & opa_mac   (Executable files to check quick test cases locally)
├── input_store   (All raw data files from other repos)
├── ebpf          (Files required for # Check eBPF capabilities)
├── ebpf-docker-compose.yml         (Docker compose for # Check eBPF capabilities)

```
First go through the setup/installation procedure.
* [Link to Check eBPF capabilities](#third)
* [Elasticsearch-Kibana-OPA Stack](#fourth)


## Setup/Installation
* Pull from docker hub
```
sudo docker pull openpolicyagent/opa
pip install inquirer
sudo docker build -f Dockerfile-OPA -t opa .
```
# Elasticsearch-Kibana-OPA Stack (EKO Stack)
<a id="fourth"></a>
## Install stack
Build `elastic-kibana` docker by following instructions given in [`../EK/README.md`](https://github.com/eBPFDevSecTools/eBPFsentinel/blob/main/sentinel/EK/README.md).
```
sudo docker-compose -f docker-compose-EKO.yml build
sudo docker-compose -f docker-compose-EKO.yml pull
```
## Execute
* Execute via docker-compose
```
sudo docker-compose -f docker-compose-EKO.yml up -d
```
* Push capabilities to `elastic`
Assume `../Opa-Engine/input_store/xdp-mptm-main_annotated_formatted.db` is the capability file.
```
cd ../EK/python3 fetchCapabilityAndUpload.py -f ../Opa-Engine/input_store/xdp-mptm-main_annotated_formatted.db -v
```
* [Test the deployment](#test)
* Cleanup environment
```
sudo docker-compose -f docker-compose-EKO.yml down
```

# Check eBPF capabilities
<a id="third"></a>
```
├── ebpf
│   ├── jsonviewer.json       (Prettyprint Capability file. Generated from ../.db)
│   ├── shortCapability.py    (Concise version of Capability file generator.)
│   ├── jsonviewer_short.json (Generated from ../input_store/.db via shortCapability.py)
│   ├── extractFromCapabilityTree.py  (Cumulative capability extractor)
│   ├── cumulativeCapabilities.json   (Generated from jsonviewer_short.json via extractFromCapabilityTree.py)
│   ├── policy.rego (Rego rules to allow certain capabilities)
│   ├── monitorElastic.py (Monitor Elastic server periodically and update cumulativeCapabilities.json)
```
### Prepare capability data file for OPA
* Take the input as `/input_store/xdp-mptm-main_annotated_formatted.db`
  * With Elastic having data
  ```
  cd ebpf; python extractFromCapabilityTree.py
  ```
  * Without Elastic take input from local file
  ```
  cd ebpf; python3 extractFromCapabilityTree.py -s ../input_store/xdp-mptm-main_annotated_formatted.db ../input_store/katran_annotated_formatted.db ../input_store/bcc_annotated_fromatted.db -d cumulativeCapabilities.json
  ```
  If you get error saying `URL = os.environ.get('URL')+'/type'`
  ```
  export `grep "URL=" ../docker-compose-EKO.yml | awk '{print $2}'`
  ```
  and re-execute the python code.
### OPA test with ebpf data and rules using a test suit
The test suit has 26 different test cases. A sample input format is as follows.
```
{
    "funcName":"encap_vlan"
}
```
  * No eBPF program name returns `False`
  * The `ALLOWED_CAPABILITIES` are as follows:
  ```
  ["pkt_go_to_next_module", "map_read","pkt_stop_processing_drop_packet"]
  ```
  Any eBPF program having a subset of the `ALLOWED_CAPABILITIES` are allowed to execute.
### Local test case evaluation
  `cd ebpf; ../opa_<OS> test .`
### With docker compose
* Host server with `sudo docker-compose -f ebpf-docker-compose.yml up`
* Test with client <a id="test"></a>
* Use curl commands to test the rules <a id="curl-commands"></a> 
  - `False` : `curl http://localhost:8181/v1/data/ebpf/allow` 
  - `True`  : `curl -X POST  --header "Content-Type: application/json" --data '{"input": {"signature": 678910}}'   http://localhost:8181/v1/data/ebpf/allow?pretty=true&explain=fail`

  - `True` :
  ```
  curl --location 'http://localhost:8181/v1/data/ebpf/allow?explain=full' \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
        "signature": 1112131415
    }
  }'
  ```
  - `False`: 
  ```
  curl --location 'http://localhost:8181/v1/data/ebpf/allow' \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
        "signature": 12345,
    }
  }'
  ```
  -`True`:
  ```
    curl --location 'http://localhost:8181/v1/data/ebpf/allow' \
  --header 'Content-Type: application/json' \
  --data '{
    "input": {
        "signature": 678910
    }
  }'
  ```
### Test with Rego Playground <a id="test-online"></a>
* Download `opa` executable using the following commands. (The linux executable is already there in `./ebpf/opa`)
```
curl -L -o opa \
https://openpolicyagent.org/downloads/v0.60.0/opa_linux_amd64; \
chmod 755 ./opa
```
* Export from [rego playground](https://play.openpolicyagent.org/) and get BUNDLE_ID (e.g. `bundles/HXD3nbpalc`)
* Set bundle ID as environment variable `export OPA_BUNDLE_ID="bundles/HXD3nbpalc"`
* Host forwarding server in localhost
` ./opa run --server --log-format text --set decision_logs.console=true --set bundles.play.polling.long_polling_timeout_seconds=45 --set services.play.url=https://play.openpolicyagent.org --set bundles.play.resource=${OPA_BUNDLE_ID}`
* In another terminal issue the curl query to this forwarding server. [List of Curl commands](#curl-commands)

### Debug policies with curl
* `curl --location 'http://localhost:8181/v1/data/ebpf/allow?explain=debug&pretty=true'   --header 'Content-Type: application/json'   --data '{
    "input": {
        "signature": 112131415
      }
    }
  }'
`
# Place holder
## Important raw data file links
* [persona_kb.json](https://github.com/eBPFDevSecTools/ebpf-projects-annotations/blob/master/asset/persona_kb.json)
* [xdp-mptm-main_annotated.db](https://github.com/eBPFDevSecTools/ebpf-projects-annotations/blob/master/projects/mptm/xdp-mptm-main_annotated.db)



# Junk (Will be removed later)
## OPA Playground Links
* (Simple eBPF test)[https://play.openpolicyagent.org/p/mCu2pPeWmX]
* (Check eBPF capabilities)[https://play.openpolicyagent.org/p/xO6rZI567f]
