File Descriptors and Redirections
A file descriptor (FD) in Unix/Linux operating systems is a reference, maintained by the kernel, that allows the system to manage Input/Output (I/O) operations. It acts as a unique identifier for an open file, socket, or any other I/O resource. In Windows-based operating systems, this is known as a file handle. Essentially, the file descriptor is the system's way of keeping track of active I/O connections, such as reading from or writing to a file.

By default, the first three file descriptors in Linux are:

Data Stream for Input
STDIN – 0
Data Stream for Output
STDOUT – 1
Data Stream for Output that relates to an error occurring.
STDERR – 2

```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % find /etc/ -name networks
/etc/networks
find: /etc/cups/certs: Permission denied
```

In this case, the error is marked and displayed with "Permission denied". We can check this by redirecting the file descriptor for the errors (FD 2 - STDERR) to "/dev/null." This way, we redirect the resulting errors to the "null device," which discards all data.

```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % find /etc/ -name networks 2>/dev/null
/etc/networks
```

Now we can see that all errors (STDERR) previously presented with "Permission denied" are no longer displayed. The only result we see now is the standard output (STDOUT), which we can also redirect to a file with the name results.txt that will only contain standard output without the standard errors.

```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % find /etc/ -name networks 2>/dev/null > results.txt
```

Redirect STDIN

As we have already seen, in combination with the file descriptors, we can redirect errors and output with greater-than character (>). This also works with the lower-than sign (<). However, the lower-than sign serves as standard input (FD 0 - STDIN). These characters can be seen as "direction" in the form of an arrow that tells us "from where" and "where to" the data should be redirected. We use the cat command to use the contents of the file "stdout.txt" as STDIN.

```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % find /etc/ -name networks 2>/dev/null 1>stdout.txt
(base) timothyalder@Timothys-MacBook-Pro ~ % cat < stdout.txt
/etc/networks
```

Redirect STDOUT and Append to a File

When we use the greater-than sign (>) to redirect our STDOUT, a new file is automatically created if it does not already exist. If this file exists, it will be overwritten without asking for confirmation. If we want to append STDOUT to our existing file, we can use the double greater-than sign (>>).

Redirect STDIN Stream to a File

We can also use the double lower-than characters (<<) to add our standard input through a stream. We can use the so-called End-Of-File (EOF) function of a Linux system file, which defines the input's end. In the next example, we will use the cat command to read our streaming input through the stream and direct it to a file called "stream.txt."

```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % cat << EOF >> stream.txt
heredoc> My
heredoc> Input
heredoc> Stream
heredoc> EOF
(base) timothyalder@Timothys-MacBook-Pro ~ % cat < stream.txt
My
Input
Stream
```

Pipes

Another way to redirect STDOUT is to use pipes (|). These are useful when we want to use the STDOUT from one program to be processed by another. One of the most commonly used tools is grep, which we will use in the next example. Grep is used to filter STDOUT according to the pattern we define. In the next example, we use the find command to search for all files in the "/etc/" directory with a ".conf" extension. Any errors are redirected to the "null device" (/dev/null). Using grep, we filter out the results and specify that only the lines containing the pattern "systemd" should be displayed.

The redirections work, not only once. We can use the obtained results to redirect them to another program. For the next example, we will use the tool called wc, which should count the total number of obtained results.

tjalder@htb[/htb]$ find /etc/ -name *.conf 2>/dev/null | grep systemd | wc -l
