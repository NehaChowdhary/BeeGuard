cp ../Opa-Engine/input_store/xdp-mptm-main_annotated data.json
## Basic Test
```
sudo docker-compose -f docker-compose-EK-stack.yml up -d
```
## With capabilities

```
python3 fetchCapabilityAndUpload.py -f ../Opa-Engine/input_store/xdp-mptm-main_annotated_formatted.db -v
```
