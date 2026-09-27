# Management

| OS | Difficulty |
| --- | --- |
| Linux | Easy |

Starting with an [`nmap`](../../../networking/docs/analysis/tools/nmap.md) scan

```
# Nmap 7.99 scan initiated Thu Sep 24 21:43:09 2026 as: nmap -sS -sV -Pn -p- -v -T5 -oN scan_results.txt 10.129.244.176
Warning: 10.129.244.176 giving up on port because retransmission cap hit (2).
Nmap scan report for 10.129.244.176
Host is up (0.23s latency).
Not shown: 65528 closed tcp ports (reset)
PORT      STATE SERVICE     VERSION
22/tcp    open  ssh         OpenSSH 9.6p1 Ubuntu 3ubuntu13.19 (Ubuntu Linux; protocol 2.0)
80/tcp    open  http        nginx 1.24.0 (Ubuntu)
443/tcp   open  ssl/http    nginx 1.24.0 (Ubuntu)
1689/tcp  open  java-rmi    Java RMI
4444/tcp  open  ssl/krb524?
37999/tcp open  java-rmi    Java RMI
50389/tcp open  ldap        (Anonymous bind OK)
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port4444-TCP:V=7.99%T=SSL%I=7%D=9/24%Time=6AB50E4A%P=x86_64-apple-darwi
SF:n23.6.0%r(LDAPSearchReq,55,"0E\x02\x01\x07d@\x04\x000<0:\x04\x0bobjectC
SF:lass1\+\x04\x03top\x04\x0bds-root-dse\x04\x17ds-cfg-root-dse-backend0\x
SF:0c\x02\x01\x07e\x07\n\x01\0\x04\0\x04\0");
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Read data files from: /usr/local/bin/../share/nmap
Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
# Nmap done at Thu Sep 24 21:50:06 2026 -- 1 IP address (1 host up) scanned in 416.41 seconds
```

The `ldap` service looks promising...

```
(base) timothyalder@Timothys-MacBook-Pro ~ % ldapsearch -x -H ldap://10.129.244.176:50389 -b "" -s base "(objectClass=*)" "*" "+"
# extended LDIF
#
# LDAPv3
# base <> with scope baseObject
# filter: (objectClass=*)
# requesting: * + 
#

#
dn:
objectClass: top
objectClass: ds-root-dse
objectClass: ds-cfg-root-dse-backend
etag: 0000000050405fb1
vendorName: Open Identity Platform Community
vendorVersion: OpenDJ Server 5.0.3
supportedLDAPVersion: 2
supportedLDAPVersion: 3
entryDN:
supportedControl: 1.2.826.0.1.3344810.2.3
supportedControl: 1.2.840.113556.1.4.1413
supportedControl: 1.2.840.113556.1.4.319
supportedControl: 1.2.840.113556.1.4.473
supportedControl: 1.2.840.113556.1.4.805
supportedControl: 1.3.6.1.1.12
supportedControl: 1.3.6.1.1.13.1
supportedControl: 1.3.6.1.1.13.2
supportedControl: 1.3.6.1.4.1.26027.1.5.2
supportedControl: 1.3.6.1.4.1.42.2.27.8.5.1
supportedControl: 1.3.6.1.4.1.42.2.27.9.5.2
supportedControl: 1.3.6.1.4.1.42.2.27.9.5.8
supportedControl: 1.3.6.1.4.1.4203.1.10.1
supportedControl: 1.3.6.1.4.1.4203.1.10.2
supportedControl: 1.3.6.1.4.1.7628.5.101.1
supportedControl: 2.16.840.1.113730.3.4.12
supportedControl: 2.16.840.1.113730.3.4.16
supportedControl: 2.16.840.1.113730.3.4.17
supportedControl: 2.16.840.1.113730.3.4.18
supportedControl: 2.16.840.1.113730.3.4.19
supportedControl: 2.16.840.1.113730.3.4.2
supportedControl: 2.16.840.1.113730.3.4.3
supportedControl: 2.16.840.1.113730.3.4.4
supportedControl: 2.16.840.1.113730.3.4.5
supportedControl: 2.16.840.1.113730.3.4.9
supportedSASLMechanisms: PLAIN
supportedSASLMechanisms: EXTERNAL
supportedSASLMechanisms: CRAM-MD5
supportedSASLMechanisms: DIGEST-MD5
entryUUID: d41d8cd9-8f00-3204-a980-0998ecf8427e
hasSubordinates: false
structuralObjectClass: ds-root-dse
subschemaSubentry: cn=schema
supportedAuthPasswordSchemes: SHA256
supportedAuthPasswordSchemes: SHA1
supportedAuthPasswordSchemes: PBKDF2-HMAC-SHA256
supportedAuthPasswordSchemes: SHA384
supportedAuthPasswordSchemes: PKCS5S2
supportedAuthPasswordSchemes: SHA512
supportedAuthPasswordSchemes: PBKDF2-HMAC-SHA512
supportedAuthPasswordSchemes: MD5
supportedAuthPasswordSchemes: PBKDF2
supportedExtension: 1.3.6.1.4.1.4203.1.11.1
supportedExtension: 1.3.6.1.4.1.4203.1.11.3
supportedExtension: 1.3.6.1.1.21.3
supportedExtension: 1.3.6.1.1.8
supportedExtension: 1.3.6.1.1.21.1
supportedExtension: 1.3.6.1.4.1.26027.1.6.3
supportedExtension: 1.3.6.1.4.1.26027.1.6.2
supportedExtension: 1.3.6.1.4.1.26027.1.6.1
supportedExtension: 1.3.6.1.4.1.1466.20037
namingContexts: dc=management,dc=htb
numSubordinates: 0
supportedFeatures: 1.3.6.1.1.14
supportedFeatures: 1.3.6.1.4.1.4203.1.5.1
supportedFeatures: 1.3.6.1.4.1.4203.1.5.2
supportedFeatures: 1.3.6.1.4.1.4203.1.5.3

# search result
search: 2
result: 0 Success

# numResponses: 2
# numEntries: 1
```

```
(base) timothyalder@Timothys-MacBook-Pro ~ % ldapsearch -x -H ldap://10.129.244.176:50389 -b "dc=management,dc=htb" "*" "+"
# extended LDIF
#
# LDAPv3
# base <dc=management,dc=htb> with scope subtree
# filter: (objectclass=*)
# requesting: * + 
#

# search result
search: 2
result: 0 Success

# numResponses: 1
```

```
(base) timothyalder@Timothys-MacBook-Pro ~ %    ldapsearch -x -H ldap://10.129.244.176:50389 -b "dc=management,dc=htb" -s base "*" "+"
# extended LDIF
#
# LDAPv3
# base <dc=management,dc=htb> with scope baseObject
# filter: (objectclass=*)
# requesting: * + 
#

# search result
search: 2
result: 0 Success

# numResponses: 1
```

Hmmm... seems to be a dead end.

Taking a look at `java-rmi`.