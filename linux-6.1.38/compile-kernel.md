Linux Version modified: 5.15.114

## Download the Source Code.

1.  Visit the official kernel website and download the latest kernel version. The downloaded file contains a compressed source code.

  	``` www.kernel.org```


2. Open the terminal and use the wget command to download the Linux kernel source code:

  	```wget https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.15.114.tar.xz```
  
  	The output shows the “saved” message when the download completes.



## Extract the Source Code. 

3. When the file is ready, run the tar command to extract the source code:

  	```tar xvf linux-5.15.114.tar.xz```
  
 	 The output displays the extracted kernel source code.


  
## Install Required Packages.

4. Install additional packages before building a kernel. To do so, run this command:

	```sudo apt-get install git fakeroot build-essential ncurses-dev xz-utils libssl-dev bc flex libelf-dev bison dwarves```

	 
	 The command we used above installs the following packages:

	  | Package | Package Description |
	  | --- | --- |
	  | git | Tracks and makes a record of all changes during development in the source code. It also allows reverting the changes. |
	  | fakeroot | Creates the fake root environment. |
	  | build-essential | Installs development tools such as C, C++, gcc, and g++. |
	  | ncurses-dev | Provides API for the text-based terminals. |
	  | xz-utils | Provides fast file compression and decompression. |
	  | libssl-dev | Supports SSL and TSL that encrypt data and make the internet connection secure. |
	  | bc (Basic Calculator)	| Supports the interactive execution of statements. |
	  | flex (Fast Lexical Analyzer Generator) | Generates lexical analyzers that convert characters into tokens. |
	  | libelf-dev | Issues a shared library for managing ELF files (executable files, core dumps and object code) |
	  | bison | Converts grammar description to a C program. |

  
  
## Configure Kernel

The Linux kernel source code comes with the default configuration. However, we can adjust it to our needs. To do so, follow the steps below:
  

5. Navigate to the linux-6.0.7 directory using the cd command:

 	 ```cd linux-5.15.114```


6. Copy the existing configuration file using the cp command:

  	```cp -v /boot/config-$(uname -r) .config```

     Add the .config file here.
 
7. To make changes to the configuration file, run the make command:

 	 ```make menuconfig```
  
  The command launches several scripts that open the configuration menu.
  
  
8. The configuration menu includes options such as firmware, file system, network, and memory settings. Use the arrows to make a selection or choose Help to learn more about the options. When we finish making the changes, select Save, and then exit the menu.


9. Modify the code in the verifier as needed and save. To go to verifier code use:

 	 ```sudo gedit kernel/bpf/verifier.c```
  
  

## Build the Kernel

10. Start building the kernel by running the following command:

	  ```make -j4```
  
  	Here 4 is the no. of processors available. The process of building and compiling the Linux kernel takes some time to complete. The terminal lists all Linux kernel components: memory management, hardware device drivers, filesystem drivers, network drivers, and process management.
 
 ### Note:
  If you are compiling the kernel on Ubuntu, you may receive the following error that interrupts the building process:
   
   		"No rule to make target 'debian/canonical-certs.pem"
   
   Disable the conflicting security certificates by executing the two commands below:

   ```scripts/config --disable SYSTEM_TRUSTED_KEYS```
    
   ```scripts/config --disable SYSTEM_REVOCATION_KEYS```
   
   The commands return no output. Start the building process again with make, and press Enter repeatedly to confirm the default options for the generation of new certificates.
  
  
  
11. Install the required modules with this command:

  	```sudo make modules_install```
  
  
12. Finally, install the kernel by typing:

  	```sudo make install```
	
 	The output shows done when finished.
  
  
  
## Update the Bootloader

The GRUB bootloader is the first program that runs when the system powers on. The make install command performs this process automatically, but you can also do it manually.


13. Update the initramfs to the installed kernel version:

   	```sudo update-initramfs -c -k 5.15.114```
    
    
14. Update the GRUB bootloader with this command:

   	```sudo update-grub```

  	The terminal prints out the process and confirmation message: done. Might need to enable os prober if it shows that os prober in not enabled using:
		
	```sudo gedit /etc/default/grub```
  
   	 Then add or uncomment "GRUB_DISABLE_OS_PROBER=false" and redo 14.
 
 
 
 ## Reboot and Verify Kernel Version
 
15. When you complete the steps above, reboot the machine.

  	```uname -mrs```
