# Regular Expressions

Just use AI...

## Exercises

1	Show all lines that do not contain the # character.
```bash
cat /etc/ssh/sshd_config | grep -v "#"


Include /etc/ssh/sshd_config.d/*
...
```

2	Search for all lines that contain a word that starts with Permit.
```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % cat /etc/ssh/sshd_config | grep -E '\bPermit\w*'
#PermitRootLogin prohibit-password
...
```

3	Search for all lines that contain a word ending with Authentication.
```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % cat /etc/ssh/sshd_config | grep -E '\w*Authentication\b' 
# Authentication:
#PubkeyAuthentication yes
...
```

4	Search for all lines containing the word Key.
```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % cat /etc/ssh/sshd_config | grep 'Key'         
# unless they are a multivalue option such as HostKey.
#HostKey /etc/ssh/ssh_host_rsa_key
...
```

5	Search for all lines beginning with Password and containing yes.
```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % cat /etc/ssh/sshd_config | grep -E '^Password|yes'
```

6	Search for all lines that end with yes.
```bash
(base) timothyalder@Timothys-MacBook-Pro ~ % cat /etc/ssh/sshd_config | grep -E 'yes$'            
#StrictModes yes
...
```
