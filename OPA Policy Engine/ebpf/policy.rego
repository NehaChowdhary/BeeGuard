package ebpf

import future.keywords.contains
import future.keywords.if
import future.keywords.in
import future.keywords.every
##############################################################################################################################
##############################################################################################################################
default allow := false
##############################################################################################################################
## Allow programs with no capability
allow if{
    x = data._default[input.signature].cumulative_capabilities
    count(x) == 0
}
######
## Allow programs having allowed capabilities
allow if{
    ALLOWED_CAPABILITIES:=["pkt_go_to_next_module", 
                            "parse_pkt_headers"]
    x = data._default[input.signature].cumulative_capabilities
    every element in x{
        element_belongs_to_list(element,ALLOWED_CAPABILITIES)
    }
}
########################################
###### 
element_belongs_to_list(element, allowed_capabilities) {
    element == allowed_capabilities[_]
}
######
containsValue(val, targetList) if{
    some c
    targetList[c] == val
}else := false
