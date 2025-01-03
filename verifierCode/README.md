# eBPF Verifier related sources
## Modifications:
```
├── Code            (Modified files which should be used with linux 6.1.38)
├────├── verifier.c (prints the return value of `bpf_check()`)
├────├── syscall.c  (has been modified for policy checking)
├────├── errno.h    (has been appeneded with a new error related to eBPF Loading)
├── linux-6.1.38
├────├── syscall.c  (Stub code WIP. Will be merged with ../code/syscall.c later)
```
## Target files 
```   
| File  | Location|
| ------------- | ------------- |
| `code/verifier.c`  | `linux-6.1.38/kernel/bpf/verifier.c`  |
| `code/syscall.c`  | `linux-6.38.1/kernel/bpf/syscall.c`  |
| `linux-6.1.38/syscall.c`  | `linux-6.38.1/kernel/bpf/syscall.c` (WIP) | 
| `code/errno.h`   | `linux-6.1.38/include/uapi/asm-generic` |
```
## Kernel compilation commands
```
VERSION=`grep '^VERSION\|^PATCHLEVEL\|^SUBLEVEL' Makefile | awk -F = '{print $2}' | tr -d ' ' | tr '\n' '.' | sed 's/.$//'`
make -j4
make modules
sudo make modueles_install
sudo make headers_install INSTALL_HDR_PATH=/usr/src/linux-$VERSION
sudo make install
```
