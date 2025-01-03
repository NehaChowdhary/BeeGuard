# BeeGuard
Explainability-based Policy Enforcement of eBPF Codes for Cloud-native Environments

# Abstract
eBPF enables loading user space code into the kernel, thereby extending the kernel functionalities in an application-aware manner. This flexibility has led to the widespread adoption
of the technology across hyperscalers and enterprises for several use cases, including observability, security, network policy enforcement, etc. In general, the safety of the loaded eBPF
programs are ensured through a kernel verifier that performs different syntactic/structural checks to secure the kernel against unwanted crashes. In this paper, we motivate the case that this verifier-based security check, while necessary, is insufficient to ensure that the deployed eBPF code complies with organizational policies. Consequently, we propose BeeGuard, a framework to understand program behavior to extract capability lists from eBPF programs. BeeGuard introduces a policy compliance layer on top of the existing verifier, and the extracted capability lists of a program are then checked against organizational policies to allow or block loading the programs. Thorough experiments across the most popular open-source eBPF tools show that BeeGuard can enforce typical enterprise policies with minimal overhead in terms of loading latency and resource utilization.

--------------------------------------------------------------------------------------

## Directory structure
```
├── CodeAnalyzer             (Takes eBPF program code and generates capabilities labels)
├── p-store                  (EK Stack deployment of p-store to store capabilities labels and organizational policies)
├── OPA Policy Engine        (Runtime Policy verification with Open Policy Agent)
├── ebpfVerifier             (Modifications in eBPF Verifier code)    
├── PolicyFetcher            (Takes eBPF byte code, generates SHA256, and checks OPA policy if the code is allowed to be executed)
```
--------------------------------------------------------------------------------------

### Attack Possibilities as per (MITRE ATT&CK v13.1) [https://attack.mitre.org/tactics/enterprise/]
```
├── Tactics
├─────├── Enterprise
├────────────├── Collection (TA0009)
├────────────────────├── AiTM (T1557 )
├────────────├── Impact (TA0040)
├────────────────────├── Endpoint DoS (T1499 )
```
