# Commands

man command, which displays the manual pages for commands and provides detailed information about their usage.

Another tool that can be useful in the beginning is apropos. Each manual page has a short description available within it. This tool searches the descriptions for instances of a given keyword.

The ls command in Linux and Unix systems is used to list the files and directories within the current folder or any specified directory, allowing you to see what's inside and manage files more effectively.

Another useful resource to get help if we have issues to understand a long command is:
https://explainshell.com/

Command	Description
whoami	Displays current username.
id	Returns users identity
hostname	Sets or prints the name of current host system.
uname	Prints basic information about the operating system name and system hardware.
pwd	Returns working directory name.
ifconfig	The ifconfig utility is used to assign or to view an address to a network interface and/or configure network interface parameters.
ip	Ip is a utility to show or manipulate routing, network devices, interfaces and tunnels.
netstat	Shows network status.
ss	Another utility to investigate sockets.
ps	Shows process status.
who	Displays who is logged in.
env	Prints environment or sets and executes command.
lsblk	Lists block devices.
lsusb	Lists USB devices
lsof	Lists opened files.
lspci	Lists PCI devices.

Which
One of the common tools is which. This tool returns the path to the file or link that should be executed.

Find
Another handy tool is find. Besides the function to find files and folders, this tool also contains the function to filter the results. We can use filter parameters like the size of the file or the date. We can also specify if we only search for files or folders.

tjalder@htb[/htb]$ find / -type f -name *.conf -user root -size +20k -newermt 2020-03-03 -exec ls -al {} \; 2>/dev/null

Option	Description
-type f	Hereby, we define the type of the searched object. In this case, 'f' stands for 'file'.
-name *.conf	With '-name', we indicate the name of the file we are looking for. The asterisk (*) stands for 'all' files with the '.conf' extension.
-user root	This option filters all files whose owner is the root user.
-size +20k	We can then filter all the located files and specify that we only want to see the files that are larger than 20 KiB.
-newermt 2020-03-03	With this option, we set the date. Only files newer than the specified date will be presented.
-exec ls -al {} \;	This option executes the specified command, using the curly brackets as placeholders for each result. The backslash escapes the next character from being interpreted by the shell because otherwise, the semicolon would terminate the command and not reach the redirection.
2>/dev/null	This is a STDERR redirection to the 'null device', which we will come back to in the next section. This redirection ensures that no errors are displayed in the terminal. This redirection must not be an option of the 'find' command.

t will take much time to search through the whole system for our files and directories to perform many different searches. The command locate offers us a quicker way to search through the system. In contrast to the find command, locate works with a local database that contains all information about existing files and folders. We can update this database with the following command.

tjalder@htb[/htb]$ sudo updatedb
If we now search for all files with the ".conf" extension, you will find that this search produces results much faster than using find.

tjalder@htb[/htb]$ locate *.conf

/etc/GeoIP.conf
/etc/NetworkManager/NetworkManager.conf
/etc/UPower/UPower.conf
/etc/adduser.conf
<SNIP>