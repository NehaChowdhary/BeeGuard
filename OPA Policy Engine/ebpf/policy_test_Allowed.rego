package ebpf_test
import data.ebpf.allow

#1
test_allow_if_blank_capability{
	allow with input as {
		"signature": 1112131415
	}
}
#2
test_allow_if_pkt_go_to_next_module{
	allow with input as {
		"signature": 678910
	}
}
