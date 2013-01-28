#!/usr/bin/env python

#
# An example python Tractor login validation script for which connects
# with an ldap server
#
# Copyright (C) 201r Pixar Animation Studios.  
# The information in this file is provided for the exclusive use of the
# licensees of Pixar.  Such users have the right to use, modify, and
# incorporate this code into other products for purposes authorized
# by the Pixar license agreement, without fee.
#
# PIXAR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS, IN NO EVENT
# SHALL PIXAR BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
#

import sys
import ldap
import getpass 

## ------------------------------------------------------------- ##

def is_ascii(s):
    return all(ord(c) < 128 for c in s)

def main ():

    # This routine expects to receive a userid, challenge, and
    # password on stdin as newline-separated strings:
    # like  "yoda\n12345 abcd\nPW\n"
    #
    # Typically the inbound "password" will actually be a 
    # site-defined hash of the real password and the challenge.
    #

    user = raw_input()
    challenge = raw_input()
    pw_hash = raw_input()

    # Simple username validation and early out.
    if not user.islower() or not is_ascii(user):
        return 1
    
    LDAP_ADDR = 'od2.london.baseblack.com'
    LDAP_CONFIG = 'uid=%s,cn=users,dc=od1,dc=london,dc=baseblack,dc=com' % user
    
    ldsrvr = ldap.open(LDAP_ADDR)
 
    cred = pw_hash.strip()
    rc = 0

    try:
        ldsrvr.simple_bind_s(LDAP_CONFIG, cred)
    except ldap.LDAPError, error_message:
        who = "uid=%s,ou=sysaccounts,o=pixar.com" % user
        try:
            ldsrvr.bind_s(LDAP_CONFIG, cred)
        except ldap.LDAPError, error_message:
            rc = 1

    del(ldsrvr)
    return rc

## ------------------------------------------------------------- ##

if __name__ == "__main__":

    rc = main()

    if 0 != rc:
        sys.exit(rc)
