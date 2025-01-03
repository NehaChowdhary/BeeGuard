# Installation
To compile and execute a bpf program.
### Requirements
1. A compatible version of Linux Kernel: BPF programs requires a Linux kernel with BPF support.
    Linux Kernel >= 6.1.38
    `wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.1.38.tar.gz`
    1. Install dependencies for compilation
    ```
    sudo apt install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bc flex libelf-dev bison
    ```
    2. Use the given `.config` file
2. Linux Kernel Headers: (Need to test this)
    You will need the kernel headers for the specific kernel version you are running in order to compiler the BPF program.
    To check if the Linux kernel headers are installed on the Ubuntu, use the foillowing command in terminal"
    ```
    dpkg -l | grep linux-headers
    ```
    This will list all the installed packages that have a name containing 'linux-headers'. 
    Look for a package with a name that starts with 'linux-headers' followed by the kernel version number. 
    For example:
    ```
    linux-headers-5.19.0-41-generic 5.19.0-41.42~22.04.1    amd64   Linux kernel headers for version 5.19.0 on 64 bit x86 SMP
    ```

    If the packages is not installed, install the linux-headers first.

3. Clang and LLVM packages: You will need to install the 'clang' and 'llvm' packages to compile the BPF program
    To check Clang version:
    ```
    $ clang --version
    ```
    Output:
    ```
    Ubuntu clang version 14.0.0-1ubuntu1
    Target: x86_64-pc-linux-gnu
    Thread model: posix
    InstalledDir: /usr/bin
    ```

    To verify that LLVM is installed:
    ```
    $ llvm-config --version
    ```
    Output:
    ```
    14.0.0
    ```    

4. BPF tools: 'bpftool' utility to load the BPF program into kernel
5. BTF(CONFIG_DEBUG_INFO_BTF) must be enabled.
6. BPF LSM(CONFIG_LSM with bpf) must be enabled. 

### Testing Environment
```
Linux Version: 5.19.17 x86_64
Clang version: Ubuntu clang version 14.0.0-1ubuntu1
bpftool version:  v7.2.0
```

#### Dependent Packages
```
$ pahole --version
v1.22
```

```
 $ which llc
/usr/bin/llc
```

### Kernel Configuration
1. Check .config file if the followling flags are enabled or not.
```
cat linux-5.19.17/.config | grep 'BPF'
cat linux-5.19.17/.config | grep 'BTF'
```
2. If the flags are not set, build your kernel with enabling below options in the configuration 

```
CONFIG_DEBUG_INFO_BTF=y
CONFIG_BPF=y
CONFIG_BPF_SYSCALL=y
CONFIG_BPF_LSM=y
CONFIF_BPF_JIT=y
CONFIG_HAVE_EBPF_JIT=y
CONFIG_BPF_EVENTS=y
CONFIG_LSM="[other LSMs],bpf"
```

3. Also, the CONFIG_LSM flag must contain bpf. This can also be controlled by boot parameters as following:

```
cat /etc/default/grub | grep 'GRUB_CMDLINE_LINUX'
```
```
. . .
GRUB_CMDLINE_LINUX="... lsm=lockdown,yama,apparmor,bpf"
. . .
```

4. To check if lsm=bpf is enabled or not
```
cat /proc/cmdline
```
It should give the following output:
```
BOOT_IMAGE=/boot/vmlinuz-5.19.0-40-generic root=UUID=1f7b445b-98a9-4465-a0ee-551d91772f56 ro lsm=lockdown,capability,landlock,yama,apparmor,bpf quiet splash
```

4. Finally update the grub to apply the changes
```
update grub
```

Refer this [link](https://phoenixnap.com/kb/build-linux-kernel) to build the linux kernel.

```
sudo find /sys/kernel/debug/tracing/events -type d | grep bpf
```
Output:
```
/sys/kernel/debug/tracing/events/bpf_test_run
/sys/kernel/debug/tracing/events/bpf_test_run/bpf_test_finish
/sys/kernel/debug/tracing/events/bpf_trace
/sys/kernel/debug/tracing/events/bpf_trace/bpf_trace_printk
/sys/kernel/debug/tracing/events/syscalls/sys_enter_bpf
/sys/kernel/debug/tracing/events/syscalls/sys_exit_bpf
```

# Quick Start (Step to attach BPF Program to the LSM hooks)
### 1. Write your LSM-BPF Prgram
Currently, we have used various open-source BPF program to verify.
Examples:
1. [bouheki: KRSI(eBPF+LSM) based Linux security auditing tool](https://github.com/mrtc0/bouheki)
2. [lsmtrace](https://github.com/lumontec/lsmtrace)
3. [Demo LSM + BPF programs](https://github.com/JeongyoonMoon/lsmbpf_demo)
4. [XDP - BPF security module to disable BPF](https://github.com/xdp-project/bpf-examples/tree/master/lsm-nobpf)

Later, we need to write our own program to attach to lsm hook.

### 2. Compilation of bpf code:
Go to and execute the command:
```
clang -g -target bpf -Wall -O2 -c lsm.c -o lsm_obj.o 
```
or (Wokring)
```
sudo clang -g -O2 -emit-llvm -c lsm_nobpf_kern.bpf.c -o - | llc -march=bpf -filetype=obj -o lsm_bpf.o
```

### 3.  Load the BPF program into kernel using the following command:
```
sudo bpftool --debug prog load ./lsm_bpf.o /sys/fs/bpf/lsm_bpf
```

Once the program is loaded, it will be attached to the lsm_hookpointname hook that you have written in your code and one can monitor the kernel log to see when it is invoked

# Some Intresting Links:
1. [eBPF Tooling](https://man7.org/linux/man-pages/man8/tc-bpf.8.html)
2. [BPF In Depth: Building BPF Programs](https://blogs.oracle.com/linux/post/bpf-in-depth-building-bpf-programs)
3. [bpf-docs](https://github.com/iovisor/bpf-docs/blob/master/eBPF.md)
4. [lsm-hooks-documentation](https://elixir.bootlin.com/linux/latest/source/include/linux/lsm_hooks.h)
5. [bpftool](https://manpages.ubuntu.com/manpages/focal/en/man8/bpftool-btf.8.html)
6. [Features of bpftool](https://qmonnet.github.io/whirl-offload/2021/09/23/bpftool-features-thread/)
7. [BPF Internals](https://www.usenix.org/system/files/lisa21_slides_gregg_bpf.pdf)
8. [retsnoop](https://github.com/anakryiko/retsnoop)


# Troubleshooting
Follow [this](https://github.com/sdsen/opened_policy_enforcer/issues/86) thread for issues related this.

## For debugging
```
sudo clang -g -O2 -target bpf -c bpf_prog.c -o bpf_prog.o
```
1. The '-g' option is used in the clang or llvm compiler is used to generate the debug information in the BPF object file i,e the BTF code. The debug info includes source file names, line numbers, and other debugging symbols that can be used to debug the BPF program.

2. To extract the BTF data from the object file
```
sudo bpftool btf dump file bpf_prog.o format c > bpf_prog.btf
```
This command dumps the BTF data from the 'bpf_prog.o' file in C format and saves it to a file called 'bpf_prog.btf'
This BTF code is used by BPF loader and verifer to ensure that the BPF program is properly validated before it is loaded into the kernel.

## Error while loading BPF program
### Issue 1:
```
sudo bpftool prog loadall bpf_prog.o /sys/fs/bpf/bpf_prog
```
Output/Error:
```
libbpf: prog 'bpf_prog': BPF program load failed: Invalid argument
libbpf: prog 'bpf_prog': -- BEGIN PROG LOAD LOG --
Tracing programs must provide btf_id
processed 0 insns (limit 1000000) max_states_per_insn 0 total_states 0 peak_states 0 mark_read 0
-- END PROG LOAD LOG --
libbpf: prog 'bpf_prog': failed to load: -22
libbpf: failed to load object 'bpf_prog.o'
Error: failed to load object file
```
This occurs when a BPF program is loaded into the kernel without a valid BTF(BPF Type Format) ID. BTF is a metadata format for BPF Program that provides information about the types of the variabled and structures used in the program. The BTF ID is the unique identifier that is assigned to the BTF data for a program.

To fix this error (Ideally), need to provide a valid BTF ID when loading the BPF program.

Solution: Try to compile the kernel wirh all the required FLAGs enabled.

### Issue 2:
While loading the object file, you may get the following error:
```
libbpf: Error loading ELF section .BTF: 0
```
Reason: This occures when the program is not compiled using -g option. [See more](https://stackoverflow.com/questions/58914021/libbpf-error-loading-elf-section-btf-0)

Solution: Give the -g option while compiling using clang
```
sudo clang -g -O2 -emit-llvm -c lsm_nobpf_kern.bpf.c -o - | llc -march=bpf -filetype=obj -o lsm_nobpf_kern_obj.o
```
Then the loading of the object file will be successful.
```
sudo bpftool --debug prog load ./lsm_nobpf_kern_obj.o /sys/fs/bpf/lsm_nobpf_kern_obj
```

### Issue 3
While loading the object file, you may get the following error:
```
sudo bpftool --debug prog load ./lsm_nobpf_kern_obj.o /sys/fs/bpf/lsm_nobpf_kern_obj
```
```
Error: failed to pin program lsm/bpf
Warning: bpftool is now running in libbpf strict mode and has more stringent requirements about BPF programs.
If it used to work for this object file but now doesn't, see --legacy option for more details.
```
Reason: A bpf program is already pinned to the same name **lsm_nobpf_kern_obj**.

Solution: Change the name of the pin location while loading:
```
sudo bpftool --debug prog load ./lsm_nobpf_kern_obj.o /sys/fs/bpf/lsm_nobpf_kern_obj_new
```

