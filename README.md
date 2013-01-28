### LDAP Login Authenticator for Pixar's Tractor Engine Web interface and Nimby

Like it or not, security is important to the management of a function renderfarm. 

Out of the box tractor comes with the ability to authenticate using the logged in user of of machine when accessing the monitoring interface. 

If instead you would like to enable access via a direct authentication against your LDAP based server, then this script can be used. 

> This can be useful when accessing the interface from external devices/networks or when the machine does not have LDAP locally setup in PAM.

#### Setup

Edit the file `trSiteLdapLoginValidator.py` with your LDAP server information. These are the 2 lines you need to edit:

    49:  LDAP_ADDR = 'od2.london.baseblack.com'
    50:  LDAP_CONFIG = 'uid=%s,cn=users,dc=od1,dc=london,dc=baseblack,dc=com' % user

Drop `trSiteLdapLoginValidator.py` into your tractor configuration directory.

    bash$ cp trSiteLdapLoginValidator.py ${TractorConfigDirectory}/trSiteLdapLoginValidator.py

Edit the crews.config file, setting the validator to the script.

    bash$ echo '"SitePasswordValidator": "python ${TractorConfigDirectory}/trSiteLdapLoginValidator.py",' >> ${TractorConfigDirectory}/crews.config

Restart the engine process. 
