A= """~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Netconf traffic yet to be allowed 

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

versa-service          is Running,          [*] process 18408
versa-infmgr           is Running,          [-] process 18387
versa-rfd              is Stopped           
versa-vmod             is Stopped           
versa-ip2user          is Stopped           
versa-imgr             is Stopped           
versa-acctmgrd         is Stopped           
versa-fltrmgr          is Running"""

while  not ("1Netconf traffic yet to be allowed" or "Stopped") in A:
    print "am in while"


print A