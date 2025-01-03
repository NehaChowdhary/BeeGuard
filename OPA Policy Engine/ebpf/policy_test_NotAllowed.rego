package ebpf_test
import data.ebpf.allow

#0
test_allow_is_false_by_default_0{
	not allow
}
#2
test_allow_if_NOT_other_capabilities{
	not allow with input as {
		"signature": 12345
	}
}