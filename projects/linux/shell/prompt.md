# Prompt Description

```bash
<username>@<hostname><current working directory>$
```

~ indicates home directory. $ indicates user

```bash
<username>@<hostname>[~]$
```

\# indicates root

```bash
root@htb[/htb]#
```

PS1 variable controls how this looks. PS1 can be customised to change whether user, computer's name, custom folder, ip address, date, time, status of last command, etc. is shown.

```bash
$
```

```bash
#
```

Using tools like script or reviewing the .bash_history file (located in the user's home directory), you can record all the commands you've used and organize them by date and time, which aids in documentation and analysis.

The prompt can be customized using special characters and variables in the shell’s configuration file (.bashrc for the Bash shell). For example, we can use: the \u character to represent the current username, \h for the hostname, and \w for the current working directory.

Special Character	Description
\d	Date (Mon Feb 6)
\D{%Y-%m-%d}	Date (YYYY-MM-DD)
\H	Full hostname
\j	Number of jobs managed by the shell
\n	Newline
\r	Carriage return
\s	Name of the shell
\t	Current time 24-hour (HH:MM:SS)
\T	Current time 12-hour (HH:MM:SS)
\@	Current time
\u	Current username
\w	Full path of the current working directory